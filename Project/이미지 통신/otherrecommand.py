import cx_Oracle as oci

def select_one_most(me):
    print("함수안에 잘들어왔다")

    con = oci.connect("food/1234@192.168.0.10:1521/orcl")
    print(con)
    # 2) 커서 얻어오기
    cursor = con.cursor()
    # 3) SQL 문장
    sql = "select m_id,m_most from member where m_id='{}'".format(me)
    # 4) sql 문장 실행
    cursor.execute(sql)

    remost = cursor.fetchall()

    print(remost)

    # 5) 커서 닫기
    cursor.close()
    # 6) 연결 닫기
    con.close()

    return remost

def select_other_most():
    print("함수안에 잘들어왔다")

    con = oci.connect("food/1234@192.168.0.10:1521/orcl")
    print(con)
    # 2) 커서 얻어오기
    cursor = con.cursor()
    # 3) SQL 문장
    sql = "select m_id,m_most from member"
    # 4) sql 문장 실행
    cursor.execute(sql)

    remost = cursor.fetchall()

    print(remost)

    # 5) 커서 닫기
    cursor.close()
    # 6) 연결 닫기
    con.close()

    return remost

def select_other_order():
    print("select_other_order함수안에 잘들어왔다")

    con = oci.connect("food/1234@192.168.0.10:1521/orcl")
    print(con)
    # 2) 커서 얻어오기
    cursor = con.cursor()
    # 3) SQL 문장
    sql = """select s.su*c.co count,s.r_menu r_menu,s.m_id m_id
            from (select r_menu r_menu,sum(R_MENU_COUNT) su,m_id m_id
            from reservation
            group by r_menu,m_id) s inner join (select r_menu r_menu,count(r_menu) co
            from reservation
            group by r_menu) c
            on s.r_menu = c.r_menu"""
    # 4) sql 문장 실행
    cursor.execute(sql)

    remost = cursor.fetchall()

    print(remost)

    # 5) 커서 닫기
    cursor.close()
    # 6) 연결 닫기
    con.close()

    return remost