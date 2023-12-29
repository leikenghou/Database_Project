# 数据库课设项目(openGauss数据库)
    本项目利用python原生库Tkinter实现界面显示，利用opengauss数据库实现数据存储。

    实现了以下功能：

    （1）玩家和厂商登录。

    （2）玩家购买、退款游戏。

    （3）厂商发行、下架游戏。

    （4）可以登录管理员账户（账户：admin  密码：admin）实现对玩家、游戏、订单和厂商的管理。

## 数据库操作：
请在数据库中执行以下sq语句（opengauss格式·）：

### 1.创建各表

（1）创建玩家账户表
```
CREATE TABLE players_account
(
		pid char(30) PRIMARY KEY,
		paccount char(30),
		ppassword char(30)
);
```
（2）创建玩家表
```
CREATE TABLE players
(
        pid CHAR(30) PRIMARY KEY,
        Pname CHAR(20) NOT NULL,
        Email CHAR(30),
        Account_balance int4,
		    Personal_Profile VARCHAR(50),
				FOREIGN KEY(pid) REFERENCES players_account(pid)
);
```
（3）创建厂商账户表
```
CREATE TABLE maufacturers_account
(
    mid char(30) PRIMARY KEY,
		maccount char(30) ,
		mpassword char(30)
);
```
（4）创建厂商表
```
CREATE TABLE manufacturers
(
        mid CHAR(30) PRIMARY KEY,
        mname CHAR(20) NOT NULL,
        Official_web CHAR(30) ,
		    income float4 DEFAULT 0,
				Manufacturers_Profile VARCHAR(50),			
				UNIQUE(mname),
				FOREIGN KEY(mid) REFERENCES maufacturers_account(mid)
);
```
（5）创建游戏表
```
CREATE TABLE games
(	
	gid CHAR(30) PRIMARY KEY,
	gname CHAR(20) NOT NULL,
	price FLOAT4 CHECK(price > 0 or price=0),
	release_date date,
	publisher CHAR(20),	
	mid CHAR(30),
	discount int4 CHECK(discount > 0 or discount<1 or discount =1),
	game_Profile VARCHAR(50)
);	
```
（6）创建厂商旗下游戏表
```
CREATE TABLE game_list
(	
    mid CHAR(30),
	gid CHAR(30),
	release_date date,
	FOREIGN KEY (gid) REFERENCES games(gid),
	FOREIGN KEY (mid) REFERENCES manufacturers(mid),
	CONSTRAINT YUESHU1 PRIMARY KEY(mid,gid)
);	
```
（7）创建玩家游戏库表
```
CREATE TABLE game_library
(	
  pid CHAR(30),
	gid CHAR(30),
	Storage_time date,
	FOREIGN KEY (gid) REFERENCES games(gid),
	FOREIGN KEY (pid) REFERENCES players(pid),
	CONSTRAINT YUESHU PRIMARY KEY(pid,gid)
);	
```
（8）创建游戏订单表
```
CREATE TABLE game_orders
(	
  goid CHAR(30) PRIMARY KEY,
	pid CHAR(30),
	gid CHAR(30),
	mid CHAR(30),
	creation_time date,
	price FLOAT,
	FOREIGN KEY (gid) REFERENCES games(gid),
	FOREIGN KEY (pid) REFERENCES players(pid),
	FOREIGN KEY (mid) REFERENCES manufacturers(mid)
);	
```
### 1.创建视图
(1)创建玩家视图
```
CREATE VIEW players_view 
AS
SELECT players.pid,pname,paccount,ppassword,email,account_balance,personal_profile
FROM players,players_account
WHERE players.pid=players_account.pid;
```
(2)创建厂商视图
```
CREATE VIEW manufacturers_view
AS
SELECT manufacturers.mid,mname,maccount,mpassword,official_web,income,manufacturers_profile
FROM manufacturers,manufacturers_account
WHERE manufacturers.mid=manufacturers_account.mid;
```
(3)创建游戏视图
```
CREATE VIEW games_view
AS
SELECT gid,gname,price,release_date,publisher,game_profile
FROM games;
```
(4)创建订单视图
```
CREATE VIEW order_view
AS
SELECT goid,pname,gname,game_orders.price,creation_time
FROM game_orders,games,players
WHERE game_orders.gid=games.gid and game_orders.pid=players.pid;
```
(5)创建玩家游戏库视图
```
CREATE VIEW player_games
AS
SELECT players.pid,gname,publisher,storage_time
FROM games,game_library,players
WHERE players.pid=game_library.pid AND games.gid=game_library.gid ;
```

(6)创建厂商旗下游戏视图
```
CREATE VIEW manufacturers_games
AS
SELECT manufacturers.mid,gname,game_list.release_date
FROM games,game_list,manufacturers
WHERE manufacturers.mid=game_list.mid AND games.gid=game_list.gid ;
```
### 1.创建索引

```
CREATE UNIQUE INDEX pi ON players(pid);
CREATE UNIQUE INDEX pai ON players_account(pid);
CREATE UNIQUE INDEX mi ON manufacturers(mid);
CREATE UNIQUE INDEX mai ON manufacturers_account(mid);
CREATE UNIQUE INDEX gi ON games(gid);
CREATE  INDEX gni ON games(gname);
CREATE UNIQUE INDEX goi ON game_orders(goid);
CREATE UNIQUE INDEX glyi ON game_library(pid,gid);
CREATE UNIQUE INDEX glti ON game_list(mid,gid);
```


### 1.创建触发器
（1）玩家删除触发器
```
CREATE OR REPLACE FUNCTION delete_related_players() RETURNS TRIGGER AS $$
BEGIN 
    
    DELETE FROM game_library WHERE pid = OLD.pid;
    DELETE FROM game_orders WHERE pid = OLD.pid;
		DELETE FROM players WHERE pid = OLD.pid;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER delete_related_players_trigger
BEFORE DELETE ON players_account
FOR EACH ROW
EXECUTE procedure delete_related_players();
```
（2）厂商删除触发器
```
CREATE OR REPLACE FUNCTION delete_related_manufacturer()
RETURNS TRIGGER AS $$
BEGIN
		DELETE FROM game_list WHERE mid = OLD.mid;
		DELETE FROM game_orders WHERE mid = OLD.mid;
    DELETE FROM games WHERE mid = OLD.mid;
    DELETE FROM manufacturers WHERE mid = OLD.mid;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER delete_related_manufacturer_trigger
BEFORE DELETE ON manufacturers_account
FOR EACH ROW
EXECUTE procedure delete_related_manufacturer();

CREATE OR REPLACE FUNCTION delete_related_manufacturer1()
RETURNS TRIGGER AS $$
BEGIN
		DELETE FROM game_list WHERE mid = OLD.mid;
		DELETE FROM game_orders WHERE mid = OLD.mid;
    DELETE FROM games WHERE mid = OLD.mid;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER delete_related_manufacturer_trigger1
BEFORE DELETE ON manufacturers
FOR EACH ROW
EXECUTE procedure delete_related_manufacturer1();
```
（3）游戏删除触发器
```
CREATE OR REPLACE FUNCTION delete_related_games() RETURNS TRIGGER AS $$
BEGIN 
    DELETE FROM game_library WHERE gid = OLD.gid;
		DELETE FROM game_list WHERE gid = OLD.gid;
    DELETE FROM game_orders WHERE gid = OLD.gid;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER delete_related_games_trigger1
BEFORE DELETE ON games
FOR EACH ROW
EXECUTE procedure delete_related_games();

```
（4）插入订单触发器
```
CREATE OR REPLACE FUNCTION players_insert_related_game() RETURNS TRIGGER AS $$
BEGIN 
    insert into game_library values(new.pid,new.gid,new.creation_time);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER players_insert_related_game_trigger
AFTER INSERT ON game_orders
FOR EACH ROW
EXECUTE procedure players_insert_related_game();
```

（5）插入游戏触发器
```
CREATE OR REPLACE FUNCTION manufacturers_insert_related_game() RETURNS TRIGGER AS $$
BEGIN 
    insert into game_list values(new.mid,new.gid,new.release_date);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER manufacturers_insert_related_game_trigger
AFTER INSERT ON games
FOR EACH ROW
EXECUTE procedure manufacturers_insert_related_game();
```
## Python操作：
请在python中执行以下语句：

**1.安装库**

```python

pip install tkinter
pip install psycopg2
```

**2.修改`method`中的连接参数**

**3.将项目中所有`finance`字段改为自己数据库的模式名称**

**4.运行`main.py`**
