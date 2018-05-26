from smtplib import *
from _mysql import *
from click import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

@command()
@argument('dbname',required=True,nargs=1)
@argument('marks_tablename',required=True,nargs=1)
@argument('student_tablename',required=True,nargs=1)
@argument('college',required=True,nargs=1)
@argument('to',required=True,nargs=1)
@argument('from_email',envvar='Email',required=False,type=str)
@argument('password',envvar='Password',required=False,type=str)
def collegereport(dbname,marks_tablename,student_tablename,college,from_email,password,to):
    try:
        server=SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login(from_email,password)
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to
        msg['Subject'] = 'College Report for ' + college
        mail_text = '<center><h2><b>College Report</b></h2><table cellspacing=10><tr><th>Student_ID</th><th>Name</th><th>Transform</th><th>From_Custom_Base26</th><th>Get_Pig_Latin</th><th>Top_Chars</th>' \
                    '<th>Total</th></tr>'
        con=connect('localhost','root','root',dbname)
        con.query('USE ' + dbname + ';')
        query = 'SELECT Student_ID,NAME,TRANSFORM,FROM_CUSTOM_BASE26,GET_PIG_LATIN,TOP_CHARS,TOTAL FROM ' + marks_tablename + ',' + student_tablename + \
                ' WHERE ' + marks_tablename + '.dbname=' + student_tablename + '.dbname AND COLLEGE="'+college+'";'
        con.query(query)
        data = con.store_result()
        n = data.num_rows()
        for i in range(n):
            row = data.fetch_row()
            for info in row:
                x = '<tr>'
                for i in info:
                    if type(i).__name__ == 'bytes':
                        i = i.decode()
                    x += '<td align=center>'+i + '</td>'
                mail_text+=x+'</tr>'
        mail_text+='</table>'
        mail_text+='<hr><h2><b>College Summary</b></h2>'
        heads=['No. of Students:','Average:','Minimum Score:','Maximum Score:']
        query = 'SELECT COUNT(*),AVG(TOTAL),MIN(TOTAL),MAX(TOTAL) FROM ' + marks_tablename + ',' + student_tablename + \
                ' WHERE ' + marks_tablename + '.dbname=' + student_tablename + '.dbname AND COLLEGE="'+college+'";'
        con.query(query)
        data = con.store_result()
        row = data.fetch_row()
        mail_text+='<table cellspacing=10>'
        for i in range(4):
            mail_text+='<tr><td align=center><b>'+heads[i]+'</b></td><td align=center>'+row[0][i]+'</td></tr>'
        mail_text+='</table><hr><h2><b>Global Summary</b></h2>'
        mail_text+='<table cellspacing=10><tr><th>College</th><th>No. of Students</th><th>Average</th><th>Minimum</th><th>Maximum</th></tr>'
        query = 'SELECT COLLEGE,COUNT(*),AVG(TOTAL),MIN(TOTAL),MAX(TOTAL) FROM ' + marks_tablename + ',' + student_tablename + \
                ' WHERE ' + marks_tablename + '.dbname=' + student_tablename + '.dbname GROUP BY COLLEGE;'
        con.query(query)
        data = con.store_result()
        n = data.num_rows()
        for i in range(n):
            row = data.fetch_row()
            for info in row:
                x = '<tr>'
                for i in info:
                    if type(i).__name__ == 'bytes':
                        i = i.decode()
                    x += '<td align=center>' + i + '</td>'
                mail_text += x + '</tr>'
        mail_text += '</table>'
        mail_text=MIMEText(mail_text,'html')
        msg.attach(mail_text)
        res=server.sendmail(from_email,to,msg.as_string())
        if(res.__len__()==0):
            echo('Report successfully emailed to '+to+' from the email: '+from_email)
    except Exception as e:
        echo(e)

if __name__=='__main__':
    collegereport()

