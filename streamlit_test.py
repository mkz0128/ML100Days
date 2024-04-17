import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model

# 创建一个标题
st.title('Welcome to NextGenPath!')

# 写一些文本
st.write("Congratulations, you are about to graduate! Please fill out the survey below to see our recommended departments for you to study : )")

# 使用form来组织输入和提交按钮
with st.form(key='student_survey'):
    # 定义各个问题及选项
    gender = st.radio("Gender ?", ("Male", "Female"))
    gpa = st.selectbox("What is your most recent GPA (Grade Point Average)? ?", (2, 3, 4, 5))
    study_hours = st.selectbox("How much time do you spend studying each day?", (1, 3, 5))
    extracurricular = st.radio("Do you participate in extracurricular activities?", ("Yes", "No"))
    competition = st.radio("Do you participate in competitions?", ("Yes", "No"))
    pc = st.radio("Are you enrolled in Advanced Placement courses in college?", ("Yes", "No"))
    q1 = st.radio("Data-driven or Creativity?", ("Data-driven", "Creativity"))
    q2 = st.radio("Indoor or Outdoor?", ("Indoor", "Outdoor"))
    q3 = st.radio("Solo or Team?", ("Solo", "Team"))
    q4 = st.radio("High pressure or Relax?", ("High pressure", "Relax"))
    q5 = st.radio("Flexible or Regular?", ("Flexible", "Regular"))
    q6 = st.radio("Specialize or Versatile?", ("Specialize", "Versatile"))
    q7 = st.radio("High salary or Job satisfaction?", ("High salary", "Job satisfaction"))

    # 提交按钮
    submit_button = st.form_submit_button(label='Submit')

# 当用户点击提交按钮后，处理输入数据
if submit_button:
    # 转换输入为数字表示
    new_conditions = np.array([[ 
        0 if gender == "Male" else 1,
        gpa,
        study_hours,
        0 if extracurricular == "Yes" else 1,
        0 if competition == "Yes" else 1,
        0 if pc == "Yes" else 1,
        0 if q1 == "Data-driven" else 1,
        0 if q2 == "Indoor" else 1,
        0 if q3 == "Solo" else 1,
        0 if q4 == "High pressure" else 1,
        0 if q5 == "Flexible" else 1,
        0 if q6 == "Specialize" else 1,
        0 if q7 == "High salary" else 1
    ]], dtype=np.int64)

    # 加载生成器模型
    generator = load_model('generator_model.h5')

    # 生成噪声输入
    noise = np.random.normal(0, 1, (1, 100))

    # 使用生成器模型生成数据
    generated_rankings = generator.predict([noise, new_conditions])

    # 部门标签
    department_labels = ['Computer Science', 'Business Administration', 'Psychology', 'Mechanical Engineering', 'Biology', 'Law', 'Fine Arts', 'Environmental Science']

    # 对每一行的排名数据进行排序
    sorted_output = []
    for rankings in generated_rankings:
        sorted_indices = np.argsort(rankings)[::-1]
        sorted_labels = [department_labels[idx] for idx in sorted_indices]
        sorted_output.append(sorted_labels)

    # 显示排序的前三名
    st.markdown("# Top 3 Departments:")
    for i in range(3):
        st.markdown(f"## {i + 1}: {sorted_output[0][i]}")
