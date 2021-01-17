# Dependencies and Setup
import pandas as pd

# File to Load (Remember to Change These)
school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas DataFrames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset.  
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
school_data

# ------- District Summary --------

# Total schools
total_schools = len(school_data_complete["school_name"].unique())

# Total students
total_students = len(school_data_complete["student_name"])

# Total budget
total_budget = school_data["budget"].sum()

# Average math score
avg_math_score = school_data_complete["math_score"].mean()

# Average reading score
avg_reading_score = school_data_complete["reading_score"].mean()

# Percentage of students passing math 
passing_math = len(school_data_complete.loc[school_data_complete["math_score"] >= 70, 
                                            ["Student ID","student_name", "math_score", "school_name"]])

total_math_scores = len(school_data_complete["math_score"])
passing_math_percentage = (passing_math/total_math_scores)*100
passing_math_percentage

# Percentage of students passing reading
passing_reading = len(school_data_complete.loc[school_data_complete["reading_score"] >= 70, 
                                            ["Student ID","student_name", "reading_score", "school_name"]])

total_reading_scores = len(school_data_complete["reading_score"])
passing_reading_percentage = (passing_reading/total_students)*100

# Percentage of students passing both math and reading
passing_math_reading = len(school_data_complete.loc[(school_data_complete["math_score"] >= 70)
                                                    & (school_data_complete["reading_score"] >= 70),
                                                    ["student_name", "math_score", "reading_score"]])
passing_math_reading_percentage = (passing_math_reading/total_students)*100

district_summary = ({"Total Schools": [total_schools],
         "Total Students": [total_students],
         "Total Budget": [total_budget],
         "Average math score": [avg_math_score],
         "Average reading score": [avg_reading_score],
         "% Passing math": [passing_math_percentage],
         "% Passing reading": [passing_reading_percentage],
         "% Passing math & reading": [passing_math_reading_percentage]
        })
district_summary_df = pd.DataFrame(district_summary)
district_summary_df["Total Budget"] = district_summary_df["Total Budget"].map("${:,.2f}".format)
district_summary_df["Total Students"] = district_summary_df["Total Students"].map("{:,}".format)
district_summary_df

# ------- School Summary --------

# School name and type 
school_name_type = school_data.set_index(['school_name'])['type']

# Total students per school 
students_per_school = school_data_complete["school_name"].value_counts()

# Total school budget
budget_per_school = school_data_complete.groupby(["school_name"]).mean()["budget"]

# Budget per student 
budget_per_student = budget_per_school/students_per_school

# Average math score per school 
avg_math_per_school = school_data_complete.groupby(["school_name"]).mean()["math_score"]
avg_reading_per_school = school_data_complete.groupby(["school_name"]).mean()["reading_score"]

# % Passing math 
passing_math_df = school_data_complete[school_data_complete["math_score"] >= 70]
passing_math_per_school = (passing_math_df.groupby("school_name").count()["math_score"]/students_per_school)*100

# % Passing reading 
passing_reading_df = school_data_complete[school_data_complete["reading_score"] >= 70]
passing_reading_per_school = (passing_reading_df.groupby("school_name").count()["reading_score"]/students_per_school)*100

# % Overall passing 
passing_overall_df = school_data_complete[(school_data_complete["math_score"] >= 70) & 
                                          (school_data_complete["reading_score"] >= 70)]
passing_overall_per_school = (passing_overall_df.groupby("school_name").count()["math_score"]/students_per_school) * 100

school_summary = ({"School Type": school_name_type, 
                   "Total Students": students_per_school, 
                   "Total School Budget": budget_per_school,
                   "Per Student Budget": budget_per_student,
                   "Average Math Score": avg_math_per_school,
                   "Average Reading Score": avg_reading_per_school,
                   "% Passing Math": passing_math_per_school,
                   "% Passing Reading": passing_reading_per_school,
                   "% Overall Passing": passing_overall_per_school
})

school_summary_df = pd.DataFrame(school_summary)
school_summary_df["Total School Budget"] = school_summary_df["Total School Budget"].map("${:,.2f}".format)
school_summary_df

# ------- Top Performing Schools (By % Overall Passing) --------

top_overall = school_summary_df.sort_values("% Overall Passing", ascending=False)
top_overall.head()

# ------- Worst Performing Schools (By % Overall Passing) --------

worst_overall = school_summary_df.sort_values("% Overall Passing", ascending=True)
worst_overall.head()

# ------- Math Scores by Grade --------

# need to find average math score for each grade 
ninth = school_data_complete[school_data_complete["grade"] == "9th"]
tenth = school_data_complete[school_data_complete["grade"] == "10th"]
eleventh = school_data_complete[school_data_complete["grade"] == "11th"]
twelfth = school_data_complete[school_data_complete["grade"] == "12th"]

ninth_math_grade = ninth.groupby(["school_name"]).mean()["math_score"]
tenth_math_grade = tenth.groupby(["school_name"]).mean()["math_score"]
eleventh_math_grade = eleventh.groupby(["school_name"]).mean()["math_score"]
twelfth_math_grade = twelfth.groupby(["school_name"]).mean()["math_score"]

by_grade = ({"9th Grade": ninth_math_grade,
            "10th Grade": tenth_math_grade,
            "11th Grade": eleventh_math_grade,
            "12th Grade": twelfth_math_grade
           })

by_grade_df = pd.DataFrame(by_grade)
by_grade_df.index.name = None 
by_grade_df

# ------- Reading Scores by Grade --------

ninth_reading_grade = ninth.groupby(["school_name"]).mean()["reading_score"]
tenth_reading_grade = tenth.groupby(["school_name"]).mean()["reading_score"]
eleventh_reading_grade = eleventh.groupby(["school_name"]).mean()["reading_score"]
twelfth_reading_grade = twelfth.groupby(["school_name"]).mean()["reading_score"]

by_grade_reading = ({"9th Grade": ninth_reading_grade,
            "10th Grade": tenth_reading_grade,
            "11th Grade": eleventh_reading_grade,
            "12th Grade": twelfth_reading_grade
           })

by_grade_reading_df = pd.DataFrame(by_grade_reading)
by_grade_reading_df.index.name = None 
by_grade_reading_df

# ------- Scores by School Spending --------

# print(school_summary_df["Per Student Budget"].max())
# print(school_summary_df["Per Student Budget"].min())

bins = [0, 580, 610, 640, 670]
group_labels = ["580 or below", "581 to 610", "611 to 640", "641 to 670"]
pd.cut(school_summary_df["Per Student Budget"], bins, labels=group_labels)
school_summary_df["Spending Ranges (Per Student)"] = pd.cut(school_summary_df["Per Student Budget"], bins, labels=group_labels)

# scores_by_spending = school_summary_df.set_index(["Spending Ranges (Per Student)"])
# scores_by_spending_df = scores_by_spending[["Average Math Score", "Average Reading Score", "% Passing Math", "% Passing Reading", "% Overall Passing"]]
avg_avg_math = school_summary_df.groupby("Spending Ranges (Per Student)").mean()["Average Math Score"]
avg_avg_reading = school_summary_df.groupby("Spending Ranges (Per Student)").mean()["Average Reading Score"]
avg_passing_math = school_summary_df.groupby("Spending Ranges (Per Student)").mean()["% Passing Math"]
avg_passing_reading = school_summary_df.groupby("Spending Ranges (Per Student)").mean()["% Passing Reading"]
avg_passing_overall = (avg_passing_math + avg_passing_reading)/2

bins_by_budget = ({"Average Math Score": avg_avg_math, 
                   "Average Reading Score": avg_avg_reading, 
                   "% Passing Math": avg_passing_math, 
                   "% Passing Reading": avg_passing_reading, 
                   "% Passing Overall": avg_passing_overall
                  })

bins_by_budget_df = pd.DataFrame(bins_by_budget)
bins_by_budget_df

# ------- Scores by School Spending --------

# print(school_summary_df["Per Student Budget"].max())
# print(school_summary_df["Per Student Budget"].min())

bins = [0, 580, 610, 640, 670]
group_labels = ["580 or below", "581 to 610", "611 to 640", "641 to 670"]
pd.cut(school_summary_df["Per Student Budget"], bins, labels=group_labels)
school_summary_df["Spending Ranges (Per Student)"] = pd.cut(school_summary_df["Per Student Budget"], bins, labels=group_labels)

# scores_by_spending = school_summary_df.set_index(["Spending Ranges (Per Student)"])
# scores_by_spending_df = scores_by_spending[["Average Math Score", "Average Reading Score", "% Passing Math", "% Passing Reading", "% Overall Passing"]]
avg_avg_math = school_summary_df.groupby("Spending Ranges (Per Student)").mean()["Average Math Score"]
avg_avg_reading = school_summary_df.groupby("Spending Ranges (Per Student)").mean()["Average Reading Score"]
avg_passing_math = school_summary_df.groupby("Spending Ranges (Per Student)").mean()["% Passing Math"]
avg_passing_reading = school_summary_df.groupby("Spending Ranges (Per Student)").mean()["% Passing Reading"]
avg_passing_overall = (avg_passing_math + avg_passing_reading)/2

bins_by_budget = ({"Average Math Score": avg_avg_math, 
                   "Average Reading Score": avg_avg_reading, 
                   "% Passing Math": avg_passing_math, 
                   "% Passing Reading": avg_passing_reading, 
                   "% Passing Overall": avg_passing_overall
                  })

bins_by_budget_df = pd.DataFrame(bins_by_budget)
bins_by_budget_df

# ------- Scores by School Size --------

# print(school_summary_df["Total Students"].max())
# print(school_summary_df["Total Students"].min())

bins = [0, 500, 2000, 3500, 5000]
school_size_labels = ["500 or below", "501 to 2000", "2001 to 3500", "3501 to 5000"]
pd.cut(school_summary_df["Total Students"], bins, labels=school_size_labels)
school_summary_df["School Size (Students)"] = pd.cut(school_summary_df["Total Students"], bins, labels=school_size_labels)

size_avg_avg_math = school_summary_df.groupby("School Size (Students)").mean()["Average Math Score"]
size_avg_avg_reading = school_summary_df.groupby("School Size (Students)").mean()["Average Reading Score"]
size_avg_passing_math = school_summary_df.groupby("School Size (Students)").mean()["% Passing Math"]
size_avg_passing_reading = school_summary_df.groupby("School Size (Students)").mean()["% Passing Reading"]
size_avg_passing_overall = (size_avg_passing_math + size_avg_passing_reading)/2

bins_by_size = ({"Average Math Score": size_avg_avg_math, 
                   "Average Reading Score": size_avg_avg_reading, 
                   "% Passing Math": size_avg_passing_math, 
                   "% Passing Reading": size_avg_passing_reading, 
                   "% Passing Overall": size_avg_passing_overall
                  })

bins_by_size_df = pd.DataFrame(bins_by_size)
bins_by_size_df

# ------- Scores by School Type --------

type_avg_math = school_summary_df.groupby("School Type").mean()["Average Math Score"]
type_avg_reading = school_summary_df.groupby("School Type").mean()["Average Reading Score"]
type_passing_math = school_summary_df.groupby("School Type").mean()["% Passing Math"]
type_passing_reading = school_summary_df.groupby("School Type").mean()["% Passing Reading"]
type_passing_overall = (type_passing_math + type_passing_reading)/2

type_summary = ({"Average Math Score": type_avg_math, 
                   "Average Reading Score": type_avg_reading, 
                   "% Passing Math": type_passing_math, 
                   "% Passing Reading": type_passing_reading, 
                   "% Passing Overall": type_passing_overall
                  })
pd.DataFrame(type_summary)