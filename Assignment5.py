from click import *
from _mysql import *
from openpyxl import *
import os

@group()
@pass_context
def mysql(context):
    con=connect('localhost','root','root')
    context.obj['conn']=con

@mysql.command()
@argument('dbname',required=True,default="db_sample",nargs=1)
@argument('students_tablename',required=True,default="Students",nargs=1)
@argument('marks_tablename',required=True,default="Marks",nargs=1)
@pass_context
def createdb(context,dbname,students_tablename,marks_tablename):
    '''Create database along with the tables'''
    con=context.obj['conn']
    query='CREATE DATABASE '+dbname+';'
    con.query(query)
    echo('Database "' + dbname + '" created successfully!')
    query = 'USE ' + dbname + ';'
    con.query(query)
    query='CREATE TABLE '+students_tablename+'(Name varchar(100),College varchar(10),Email varchar(100),DBNAME varchar(20) PRIMARY KEY);'
    con.query(query)
    echo('Students Table "' + students_tablename + '" created successfully!')
    query='CREATE TABLE '+marks_tablename+'(Student_ID varchar(100) PRIMARY KEY,DBNAME varchar(20),TRANSFORM integer,FROM_CUSTOM_BASE26 integer,' \
                                'GET_PIG_LATIN integer,TOP_CHARS integer,TOTAL integer,FOREIGN KEY(DBNAME) REFERENCES '+students_tablename+'(DBNAME));'
    con.query(query)
    echo('Marks Table "'+marks_tablename+'" created successfully!')

@mysql.command()
@argument('dbname',required=True,default='db_sample',nargs=1)
@pass_context
def dropdb(context,dbname):
    '''Drop the database along with all its tables \n Arguments: Database Name'''
    con=context.obj['conn']
    query='DROP DATABASE '+dbname+';'
    con.query(query)
    echo('Database "'+dbname+'" dropped successfully!')

@mysql.command()
@argument('dbname',required=True,nargs=1)
@argument('marks_tablename',required=True,nargs=1)
@argument('student_tablename',required=True,nargs=1)
@argument('marks_filename',required=True,nargs=1)
@argument('students_filename',required=True,nargs=1)
@pass_context
def importdata(context,dbname,marks_tablename,student_tablename,marks_filename,students_filename):
    '''Import data to the specified database tables from the specified files. \n Arguments (in order): Database Name, Marks Table Name, Students Table Name, Marks File Path, Students File Path'''
    con=context.obj['conn']
    query='USE '+dbname+';'
    con.query(query)
    marks_wb=load_workbook(marks_filename)
    students_wb=load_workbook(students_filename)
    marks_sheet=marks_wb['Sheet']
    students_sheet=students_wb['Current']
    marks_rows=list(marks_sheet.rows)[1:]
    students_rows=list(students_sheet.rows)[1:]
    for row in students_rows:
        query='INSERT INTO '+student_tablename+' VALUES('
        for cell in row[:-1]:
            query+='"'+cell.value+'",'
        query+='"'+row[-1].value.lower()+'");'
        con.query(query)
    echo('Data import to "'+student_tablename+'" successful!\n'+str(students_rows.__len__())+' records inserted.')
    for row in marks_rows:
        query = 'INSERT INTO ' + marks_tablename + ' VALUES("'+row[0].value+'","'+row[0].value.split('_')[2]+'",'
        for cell in row[1:-1]:
            query +=cell.value+','
        query +=row[-1].value.lower() + ');'
        con.query(query)
    echo('Data import to "' + marks_tablename + '" successful!\n' + str(
        marks_rows.__len__()) + ' records inserted.')

@mysql.command()
@argument('dbname',required=True,nargs=1)
@argument('marks_tablename',required=True,nargs=1)
@argument('student_tablename',required=True,nargs=1)
@pass_context
def collegestats(context,dbname,marks_tablename,student_tablename):
    '''Displays college statistics. Arguments (in order): Database Name, Marks Table Name, Students Table Name'''
    con=context.obj['conn']
    con.query('USE '+dbname+';')
    query='SELECT COLLEGE,COUNT(*),AVG(TOTAL),MIN(TOTAL),MAX(TOTAL) FROM '+marks_tablename+','+student_tablename+\
          ' WHERE '+marks_tablename+'.dbname='+student_tablename+'.dbname GROUP BY COLLEGE;'
    con.query(query)
    try:
        data=con.store_result()
        n=data.num_rows()
        echo('College Count Average Minimum Maximum')
        for i in range(n):
            row=data.fetch_row()
            for info in row:
                x=''
                for i in info:
                    if type(i).__name__=='bytes':
                        i=i.decode()
                    x+=i+'\t'
                echo(x)
    except Exception as e:
        echo(e)

if __name__=='__main__':
    mysql(obj={})
