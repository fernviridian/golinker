drop table if exists urls;
create table urls (
  id integer primary key autoincrement,
  shorturl text not null,
  longurl text not null
);
