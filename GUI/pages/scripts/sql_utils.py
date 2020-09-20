# 2020/07/12
# SQL Functions

import pyodbc as sql
import textwrap as tw

try:
    # Calling from this file
    from queries import Queries as q
except:
    pass

try:
    # Calling from another file
    from scripts.queries import Queries as q
except:
    from pages.scripts.queries import Queries as q


class db():
    def __init__(self):
        self.server = 'localhost'
        self.database = 'fanfiction'
        self.un = 'username'
        self.pw = 'password'
        self.cnxn = sql.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};' +
            'SERVER=' + self.server +
            ';DATABASE=' + self.database +
            ';UID=' + self.un + ';PWD=' + self.pw
        )
        self.cursor = self.cnxn.cursor()

    def processResults(self):
        columns = [column[0] for column in self.cursor.description]
        results = [dict(zip(columns, row)) for row in self.cursor.fetchall()]

        return results

    def getFolders(self):
        pass

    def getBrowseInfo(self):
        pass

    def getCategorySource(self):
        self.cursor.execute("SELECT * FROM Category_Source")
        results = self.processResults()

        res = {}

        for row in results:
            res[row['Src_Name']] = row['Src_Id']

        return res

    # Retrieve list of categories for a specific category_source
    def getCategories(self, srcId = 0):
        ffnCategories = tw.dedent(q.category_query(srcId))

        # TODO: Check to see if passing a parameter is ok even if the query isn't parameterized
        if srcId > 0:
            self.cursor.execute(ffnCategories, srcId)
        else:
            self.cursor.execute(ffnCategories)

        results = self.processResults()

        res = {}

        for row in results:
            res[row['Cat_Name']] = row['Cat_Id']

        return res

    # Retrieve story ratings
    def getRatings(self):
        self.cursor.execute("SELECT Rating_Id, Rating_Code AS Rating, Rating_Short_Desc AS Description FROM Rating WHERE Rat_Suspend = 0")
        results = self.processResults()

        # RatingId = []
        # Rating = []
        # RatingDesc = []

        # for row in results:
        #     RatingId.append(row['Rating_Id'])
        #     Rating.append(row['Rating'])
        #     RatingDesc.append(row['Desc'])

        # return RatingId, Rating, RatingDesc
        return results

    def getSource(self):
        self.cursor.execute("SELECT Src_Id, Src_Name FROM Source_Platform WHERE Src_Suspend = 0")
        results = self.processResults()

        res = {}

        for row in results:
            res[row['Src_Name']] = row['Src_Id']

        return res

if __name__ == '__main__':
    d = db()
    sources = d.getSource()
    print(sources)
