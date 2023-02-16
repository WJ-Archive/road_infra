CREATE DATABASE dbdb default CHARACTER SET UTF8;
SHOW DATABASES;
select * from user;
use dbdb;



CREATE TABLE gnss_tb(
	id			 INT NOT NULL AUTO_INCREMENT,
    gp_lat		 float8,
    gp_lon		 float8,
    speed		 float,
    time_stamp	 timestamp,
    PRIMARY KEY (id)
)ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE env_tb(
	id			 INT NOT NULL AUTO_INCREMENT,
    ev_lux		 float,
    ev_temp		 float,
    ev_hum		 float,
	time_stamp	 timestamp,
    gnss_id		 int not null,
    PRIMARY KEY (id),
	FOREIGN KEY (gnss_id) REFERENCES gnss_tb (id)
)ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE imu_tb(
	id				INT NOT NULL auto_increment,
	ev_imu_x		float,
    ev_imu_y		float,
    ev_imu_z		float,
    time_stamp		timestamp,
    gnss_id			int not null,
    PRIMARY KEY (id),
	FOREIGN KEY (gnss_id) REFERENCES gnss_tb (id)
)ENGINE=InnoDB Charset=utf8;

CREATE TABLE det_tb(
	id				INT NOT NULL auto_increment,
	sign_name		varchar(50),
    sign_class		INT,
    recog			float,
    x				float,
    y				float,
    w				float,
    h				float,
    frame			INT,    
    img_path		varchar(100),
    time_stamp		timestamp,
    gnss_id			int not null,
    PRIMARY KEY (id),
	FOREIGN KEY (gnss_id) REFERENCES gnss_tb (id)
)ENGINE=InnoDB Charset=utf8;

CREATE TABLE road_tb(
	id					INT NOT NULL auto_increment,
    recv_num			int,
    rd_temp				float,
    rd_dewp				float,
	rd_hum				float,
    waterfilm_h			float,
    rd_status			float,
    rd_ice_per			float,
    rd_fric				float,
    rd_status_str		varchar(20),
	battV				float,
    ptemp				float,
    time_stamp			timestamp,
    gnss_id				int not null,
    PRIMARY KEY (id),
    FOREIGN KEY (gnss_id) REFERENCES gnss_tb(id)
)ENGINE=InnoDB Charset=utf8;

CREATE TABLE pthole_tb(
	id					INT NOT NULL auto_increment,
    msg_uuid			varchar(36),
	obj_id				long,
    obj_type			int,
	obj_image			varchar(512),
    obj_time			timestamp(3), 
    pt_h_max			float,
    time_stamp			timestamp,
    gnss_id				int not null,
    PRIMARY KEY (id),
    FOREIGN KEY (gnss_id) REFERENCES gnss_tb(id)
)ENGINE=InnoDB Charset=utf8;

CREATE TABLE pt_frame_tb(
	id					INT NOT NULL auto_increment,
    pt_x				float,
	pt_w				float,
	pth_h_avg			float,
    pthole_id			int not null,
    PRIMARY KEY (id),
    FOREIGN KEY (pthole_id) REFERENCES pthole_tb(id)
)ENGINE=InnoDB Charset=utf8;

select * from gnss_tb order by id;
select * from imu_tb order by id;
select * from env_tb order by id;
select * from det_tb order by id;
select * from road_tb order by id;
select * from pthole_tb order by id;
select * from pt_frame_tb order by id;
select x, y, w, h from det_tb where frame = 1 group by frame;
INSERT INTO gnss_tb (gp_lat, gp_lon, speed, time_stamp) values(0.0, 0.0, 0.0, '2022-06-23 11:28:02');

select x.*, y.*, z.* from imu_tb x join env_tb y on x.id=y.id join road_tb z on y.id=z.id;
select x.*, y.*, z.* from imu_tb x join env_tb y join road_tb z;
select x.*, y.*, z.* from imu_tb x, env_tb y, road_tb z;
