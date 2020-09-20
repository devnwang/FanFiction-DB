# 2020/08/11
# Query Statements

import textwrap

class Queries():
    @staticmethod
    def category_query(srcId):
        q = """
            SELECT Cat_Id, Cat_Name 
            FROM Category
        """
        
        if srcId > 0:
            q += """
            WHERE Src_Id = ?
            """
        return q

if __name__ == "__main__":
    query = Queries()
    q = query.category_query(0)
    print(q)