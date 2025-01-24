import requests as rq
from Course import Course
from Section import Section
from Bundle import Bundle
from Lecture import Lecture
import pandas as pd


def data():
    collegs = [
        "Science",
        "Arts",
        "Engineering",
        "Agriculture",
        "Medicine",
        "Education",
        "Law",
        "Nursing",
        "Economics",
        "CPS",
    ]
    lst = []
    for college in collegs:
        url = f"https://github.com/Mohammed-Alabri/SQU-Timetable-Maker/raw/refs/heads/main/data/{college}.xls"
        file = rq.get(url).content
        df = pd.ExcelFile(file).parse("Sheet1")
        df = df.dropna(subset=["From Time", "Day", "To Time"])
        df = df.fillna("")
        df["Section Num"] = df["Section Num"].astype(int)
        df = df.astype(str)
        lst.append(df)
    final_df = pd.concat(lst)

    return final_df





def courses_data():
    bundle = Bundle()
    df = data()
    for index, row in df.iterrows():
        if not bundle.find_course(row["Course Code"]):
            course = Course(row["Course Code"], row["Course Name"])
            bundle.add_course(course)
            sec = Section(
                course,
                row["Section Num"],
                Lecture(
                    row["Section Num"],
                    row["Day"],
                    row["From Time"],
                    row["To Time"],
                    row["Hall Name"],
                ),
                row["Instructor Name"],
            )

            course.add_section(sec)
        elif not bundle.find_course(row["Course Code"]).getsec(str(row["Section Num"])):
            course = bundle.find_course(row["Course Code"])
            sec = Section(
                course,
                str(row["Section Num"]),
                Lecture(
                    str(row["Section Num"]),
                    row["Day"],
                    row["From Time"],
                    row["To Time"],
                    row["Hall Name"],
                ),
                row["Instructor Name"],
            )

            course.add_section(sec)
        else:
            sec = bundle.find_course(row["Course Code"]).getsec(str(row["Section Num"]))
            sec.add_lecture(
                Lecture(
                    str(row["Section Num"]),
                    row["Day"],
                    row["From Time"],
                    row["To Time"],
                    row["Hall Name"],
                )
            )

    return bundle
