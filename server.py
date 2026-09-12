import os,json,sqlite3,random,string,time,re
import tornado.web,tornado.websocket,tornado.ioloop
PORT=int(os.getenv('PORT','5000'));DB=os.getenv('DB_PATH','users.db');ADMIN_KEY=os.getenv('ADMIN_KEY','change-me');rooms={};sockets={}
def db():
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row;return c
def init_db():
 c=db();c.executescript('CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY,name TEXT NOT NULL,username TEXT UNIQUE,wins INTEGER DEFAULT 0,losses INTEGER DEFAULT 0,draws INTEGER DEFAULT 0,created REAL);CREATE TABLE IF NOT EXISTS friends(user_id TEXT,friend_id TEXT,status TEXT,PRIMARY KEY(user_id,friend_id));CREATE TABLE IF NOT EXISTS challenges(id INTEGER PRIMARY KEY AUTOINCREMENT,from_id TEXT,to_id TEXT,room TEXT,from_name TEXT,created REAL);');c.commit();c.close()
def j(h,d,status=200):h.set_status(status);h.set_header('Content-Type','application/json');h.write(json.dumps(d))
def body(h):
 try:return json.loads(h.request.body or '{}')
 except:return {}
def user(uid,name=None):
 c=db();r=c.execute('SELECT * FROM users WHERE id=?',(uid,)).fetchone()
 if not r:
  c.execute('INSERT INTO users(id,name,created) VALUES(?,?,?)',(uid,(name or 'Player')[:30],time.time()));c.commit();r=c.execute('SELECT * FROM users WHERE id=?',(uid,)).fetchone()
 c.close();return dict(r)
def result(b):
 for a,z,q in ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)):
  if b[a] and b[a]==b[z]==b[q]:return b[a]
 return 'D' if all(b) else None
def stats(w,p):
 if w not in ('X','O','D'):return
 c=db()
 for m,uid in p.items():c.execute('UPDATE users SET wins=wins+1 WHERE id=?',(uid,)) if w==m else c.execute('UPDATE users SET losses=losses+1 WHERE id=?',(uid,)) if w in ('X','O') else c.execute('UPDATE users SET draws=draws+1 WHERE id=?',(uid,))
 c.commit();c.close()
class API(tornado.web.RequestHandler):
 def set_default_headers(self):self.set_header('Access-Control-Allow-Origin','*');self.set_header('Access-Control-Allow-Headers','Content-Type,X-Admin-Key');self.set_header('Access-Control-Allow-Methods','GET,POST,OPTIONS')
 def options(self):self.set_status(204)
 def get(self):
  p=self.request.path
  if p=='/api/health':return j(self,{'ok':True,'service':'tictactoe-online'})
  if p=='/api/users':
   c=db();r=c.execute('SELECT id,name,username,wins,losses,draws FROM users ORDER BY wins DESC,losses ASC LIMIT 100').fetchall();c.close();return j(self,[dict(x) for x in r])
  if p=='/api/user/status':
   u=user(self.get_argument('userId',''));return j(self,{'hasProfile':bool(u.get('username')),**u})
  if p=='/api/user/check-username':
   q=self.get_argument('username','').strip();c=db();r=c.execute('SELECT 1 FROM users WHERE lower(username)=lower(?)',(q,)).fetchone();c.close();return j(self,{'available':not bool(r)})
  if p=='/api/friends':
   c=db();r=c.execute('SELECT u.id,u.name,u.username,u.wins,u.losses,u.draws,f.status FROM friends f JOIN users u ON u.id=f.friend_id WHERE f.user_id=?',(self.get_argument('userId',''),)).fetchall();c.close();return j(self,[dict(x) for x in r])
  if p=='/api/challenges/incoming':
   c=db();r=c.execute('SELECT * FROM challenges WHERE to_id=? ORDER BY created DESC',(self.get_argument('userId',''),)).fetchall();c.close();return j(self,[dict(x) for x in r])
  if p=='/api/admin/verify':return j(self,{'ok':self.request.headers.get('X-Admin-Key','')==ADMIN_KEY})
  if p=='/api/admin/users':
   if self.request.headers.get('X-Admin-Key','')!=ADMIN_KEY:return j(self,{'error':'Forbidden'},403)
   c=db();r=c.execute('SELECT id,name,username,wins,losses,draws FROM users ORDER BY created DESC').fetchall();c.close();return j(self,[dict(x) for x in r])
  return j(self,{'error':'Not found'},404)
 def post(self):
  p=self.request.path;d=body(self)
  if p=='/api/user/register':
   uid=str(d.get('userId','')).strip();un=str(d.get('username','')).strip();name=str(d.get('displayName','')).strip()
   if not uid or not name or not re.fullmatch(r'[A-Za-z0-9_]{3,20}',un):return j(self,{'error':'Invalid profile'},400)
   c=db()
   try:c.execute('INSERT INTO users(id,name,username,created) VALUES(?,?,?,?)',(uid,name,un,time.time()));c.commit()
   except sqlite3.IntegrityError:return j(self,{'error':'Username has been taken'},409)
   finally:c.close()
   return j(self,{'ok':True})
  if p=='/api/friends/request':
   c=db();c.execute('INSERT OR REPLACE INTO friends VALUES(?,?,?)',(d.get('fromId'),d.get('toId'),'pending'));c.commit();c.close();return j(self,{'ok':True})
  if p=='/api/friends/respond':
   c=db();uid=d.get('userId');fid=d.get('friendId');
   if d.get('accept'):c.execute('INSERT OR REPLACE INTO friends VALUES(?,?,?)',(uid,fid,'accepted'));c.execute('INSERT OR REPLACE INTO friends VALUES(?,?,?)',(fid,uid,'accepted'))
   else:c.execute('DELETE FROM friends WHERE user_id=? AND friend_id=?',(uid,fid))
   c.commit();c.close();return j(self,{'ok':True})
  if p=='/api/challenges/send':
   c=db();c.execute('INSERT INTO challenges(from_id,to_id,room,from_name,created) VALUES(?,?,?,?,?)',(d.get('fromId'),d.get('toId'),d.get('roomCode'),d.get('fromName','Player'),time.time()));c.commit();c.close();return j(self,{'ok':True})
  if p=='/api/challenges/dismiss':
   c=db();c.execute('DELETE FROM challenges WHERE id=?',(d.get('id'),));c.commit();c.close();return j(self,{'ok':True})
  if p=='/api/admin/delete-user':
   if self.request.headers.get('X-Admin-Key','')!=ADMIN_KEY:return j(self,{'error':'Forbidden'},403)
   c=db();c.execute('DELETE FROM users WHERE id=?',(d.get('userId'),));c.commit();c.close();return j(self,{'ok':True})
  if p=='/api/admin/reset-platform':
   if self.request.headers.get('X-Admin-Key','')!=ADMIN_KEY:return j(self,{'error':'Forbidden'},403)
   c=db();c.executescript('DELETE FROM users;DELETE FROM friends;DELETE FROM challenges;');c.commit();c.close();return j(self,{'ok':True})
  return j(self,{'error':'Not found'},404)
class WS(tornado.websocket.WebSocketHandler):
 def check_origin(self,origin):return True
 def open(self):self.uid=self.get_argument('userId','guest-'+str(id(self)));sockets[self.uid]=self;self.room=None
 def sendj(self,d):
  try:self.write_message(json.dumps(d))
  except:pass
 def on_message(self,msg):
  try:d=json.loads(msg)
  except:return
  t=d.get('type')
  if t=='create':
   code=''.join(random.choice(string.ascii_uppercase+string.digits) for _ in range(5));rooms[code]={'board':['']*9,'turn':'X','players':{'X':self.uid},'names':{'X':d.get('name','Player')}};self.room=code;self.sendj({'type':'created','code':code});return
  if t=='join':
   code=str(d.get('code','')).upper();r=rooms.get(code)
   if not r:return self.sendj({'type':'error','message':'Room not found'})
   if 'O' in r['players']:return self.sendj({'type':'error','message':'Room is full'})
   r['players']['O']=self.uid;r['names']['O']=d.get('name','Player');self.room=code;self.broadcast({'type':'start','code':code,'board':r['board'],'turn':r['turn']});return
  if not self.room or self.room not in rooms:return
  r=rooms[self.room]
  if t=='move':
   mark=next((m for m,u in r['players'].items() if u==self.uid),None);i=d.get('index')
   if mark!=r['turn'] or not isinstance(i,int) or i<0 or i>8 or r['board'][i]:return
   r['board'][i]=mark;w=result(r['board']);r['turn']='O' if r['turn']=='X' else 'X';self.broadcast({'type':'update','code':self.room,'board':r['board'],'turn':r['turn']})
   if w:stats(w,r['players']);self.broadcast({'type':'gameover','code':self.room,'board':r['board'],'winner':w})
  elif t=='restart':r['board']=['']*9;r['turn']='X';self.broadcast({'type':'start','code':self.room,'board':r['board'],'turn':'X'})
  elif t=='chat':self.broadcast({'type':'chat','name':str(d.get('name','Player'))[:30],'text':str(d.get('text',''))[:200]})
 def broadcast(self,d):
  for uid in rooms.get(self.room,{}).get('players',{}).values():
   if uid in sockets:sockets[uid].sendj(d)
 def on_close(self):
  sockets.pop(getattr(self,'uid',''),None)
  if self.room in rooms:
   r=rooms[self.room];r['players']={m:u for m,u in r['players'].items() if u!=self.uid};self.broadcast({'type':'opponent_left'})
   if not r['players']:rooms.pop(self.room,None)
class Static(tornado.web.StaticFileHandler):
 def set_extra_headers(self,path):self.set_header('Cache-Control','no-cache')
def make_app():return tornado.web.Application([(r'/api/ws',WS),(r'/api/(.*)',API),(r'/(.*)',Static,{'path':os.path.dirname(os.path.abspath(__file__)),'default_filename':'index.html'})],debug=False)
if __name__=='__main__':init_db();make_app().listen(PORT,address='0.0.0.0');print('TicTacToe server listening on',PORT);tornado.ioloop.IOLoop.current().start()
