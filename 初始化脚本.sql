use temp_control_system;
set charset utf8;
insert into `温控系统_user` (user_name, password ,user_type)
values ('1001','1001','H'),
	   ('1002','1002','A'),
       ('1003','1003','F'),
       ('1004','1004','C');
       
insert into `温控系统_airc` (room_num)
values ('1001'),('1002'),('1003'),('1004'),('1005');