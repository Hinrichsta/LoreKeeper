import os
import datetime
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, MetaData, Table, Column, Integer, String, DateTime, ForeignKey, Date, func, Float, text
from typing import List, Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
import pymssql

load_dotenv('.env')

LoreData = URL.create(
    "mssql+pymssql",
    username=os.getenv('SQL_USER'),
    password=os.getenv('SQL_PASS'),
    host=os.getenv('SQL_SERVER'),
    database=os.getenv('SQL_DATABASE')
)

dbEngine = create_engine(LoreData)
meta_obj = MetaData()

class Base(DeclarativeBase):
    pass

class Party(Base):
    __tablename__ = 'Party'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), nullable=True)
    player: Mapped[str] = mapped_column(String(), nullable=True)
    role: Mapped[str] = mapped_column(String(), nullable=True)
    race: Mapped[str] = mapped_column(String(), nullable=True)
    joinDate: Mapped[datetime.datetime] = mapped_column(nullable=False)
    leaveDate: Mapped[datetime.datetime] = mapped_column(nullable=True)
    items: Mapped[list["Magic_Items"]] = relationship()

class AR(Base):
    __tablename__ = 'AR'
    id: Mapped[int] = mapped_column(primary_key=True)
    irl_date: Mapped[datetime.datetime] = mapped_column(nullable=False)
    ig_date: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(String())
    pp: Mapped[int] = mapped_column(Integer(), nullable=True)
    gp: Mapped[int] = mapped_column(Integer(), nullable=True)
    sp: Mapped[int] = mapped_column(Integer(), nullable=True)
    cp: Mapped[int] = mapped_column(Integer(), nullable=True)
    members: Mapped[List["AR_Members"]] = relationship()

class AR_Members(Base):
    __tablename__ = 'AR_Member_Transactions'
    AR_id: Mapped[int] = mapped_column(ForeignKey("AR.id"), primary_key=True)
    Party_id: Mapped[int] = mapped_column(ForeignKey("Party.id"), primary_key=True)
    notes: Mapped[Optional[str]]
    trans: Mapped["AR"] = relationship()

class AP(Base):
    __tablename__ = 'AP'
    id: Mapped[int] = mapped_column(primary_key=True)
    irl_date: Mapped[datetime.datetime] = mapped_column(nullable=False)
    ig_date: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(String())
    pp: Mapped[int] = mapped_column(Integer(), nullable=True)
    gp: Mapped[int] = mapped_column(Integer(), nullable=True)
    sp: Mapped[int] = mapped_column(Integer(), nullable=True)
    cp: Mapped[int] = mapped_column(Integer(), nullable=True)
    members: Mapped[List["AP_Members"]] = relationship()

class AP_Members(Base):
    __tablename__ = 'AP_Member_Transactions'
    AP_id: Mapped[int] = mapped_column(ForeignKey("AP.id"), primary_key=True)
    Party_id: Mapped[int] = mapped_column(ForeignKey("Party.id"), primary_key=True)
    notes: Mapped[Optional[str]]
    trans: Mapped["AP"] = relationship()

class Magic_Items(Base):
    __tablename__ = 'Magic_Items'
    id: Mapped[int] = mapped_column(primary_key=True)
    irl_date: Mapped[datetime.datetime] = mapped_column(nullable=False)
    ig_date: Mapped[str] = mapped_column(String(32))
    name: Mapped[str] = mapped_column(String())
    notes: Mapped[str] = mapped_column(String(), nullable=True)
    rarity: Mapped[str] = mapped_column(String(), nullable=True)
    make: Mapped[str] = mapped_column(String(), nullable=True)
    link: Mapped[str] = mapped_column(String(), nullable=True)
    Status: Mapped[str] = mapped_column(String())
    owner: Mapped[int] = mapped_column(ForeignKey(Party.id))

class Ships(Base):
    __tablename__ = 'Ships'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())
    type: Mapped[str] = mapped_column(String())
    size: Mapped[str] = mapped_column(String())
    crew: Mapped[list["Crew"]] = relationship()

class Crew(Base):
    __tablename__ = 'Crew'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())
    race: Mapped[str] = mapped_column(String())
    stat_block: Mapped[str] = mapped_column(String())
    ship_id: Mapped[int] = mapped_column(ForeignKey(Ships.id))

Base.metadata.create_all(dbEngine)

Lore_Session = Session(dbEngine)

Test = Lore_Session.execute(text("Select *, (CAST(total AS float)/CAST(membercount AS float)) as Split FROM (Select id, CAST(irl_date as DATE) as irl_date, ig_date, description, pp, gp, sp, cp, ((pp*10) + gp + (sp/10) + (cp/100)) as total, COUNT(AR_Member_Transactions.AR_id) as membercount, STRING_AGG(AR_Member_Transactions.Party_id, ',') as members FROM AR LEFT JOIN AR_Member_Transactions ON AR.id = AR_Member_Transactions.AR_id GROUP BY AR.id, AR.irl_date, ar.ig_date, ar.description, ar.pp, ar.gp, ar.sp, ar.cp) tbl")).all()

#for t in Test:
#    print(t)
#    split = t[10].split(',')
#    for s in split:
#        Name = (Lore_Session.execute(text(f"SELECT name FROM Party WHERE id = {s}")).all())[0][0]
#        print(f"{s},{Name}")
#
#names = []
#for t in Test:
#    t[0]
#    split = t[10].split(',')
#    temp = ''
#    i=0
#    while i < len(split):
#        temp += str((Lore_Session.execute(text(f"SELECT name FROM Party WHERE id = {split[i]}")).all())[0][0])
#        if i == (len(split) - 1): 
#            pass
#        else:
#            temp += ', '
#        i += 1
#    names.append(temp)
#for n in names:
#    print(n)