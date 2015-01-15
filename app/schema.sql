drop table if exists to_dos;
create table to_dos (
	id integer primary key autoincrement,
	item text not null,
	entry_time numeric not null,
	is_completed boolean not null,
	completed_time numeric
	);