import pandas as pd
import streamlit as st
from datetime import date
import helper
import display_functions as dsf
import os


# Generating DataFrame
# noinspection PyBroadException

try:
    projects = pd.read_excel(f'projects.xlsx')
except Exception as e:
    projects = pd.DataFrame(
        columns=['Name', 'Due Date', 'Priority', 'Completed Tasks', 'Total Tasks', 'Completed', 'descr'])
projects = helper.clean_df(projects)  # function to clean data
tabs = st.tabs(['My Projects', 'Add Project'])
projects = helper.dates_in_data(projects)  # function to format dates
# Adding a project and updating xlsx
with tabs[1]:
    name = st.text_input('Project Name').capitalize()
    description = st.text_area('Description')
    today = date.today()
    due = st.date_input('Due Date', min_value=today)
    col1, col2 = st.columns(2)
    with col1:
        priority = st.slider('Project Priority', min_value=1, max_value=5, step=1)

    if st.button('submit'):
        dsf.progress()
        if name in list(projects['Name']):
            st.error('Project already exists')

        else:
            st.success('Project Added')
            projects.loc[len(projects.index)] = [name, due, priority, 0, 0, 0, description, 0, 0, 0, 0]
            projects = helper.dates_in_data(projects)
            temp_data = pd.DataFrame(columns=['Task', 'Status', 'Date completed'])
            projects.to_excel('projects.xlsx')
            temp_data.to_excel(f'projects_{name}.xlsx')

# select box for projects
project_list = list(projects['Name'])
project_list.insert(0, 'All projects')

with tabs[0]:
    proj = st.sidebar.selectbox('Manage: ', project_list)

    # Displaying all projects
    if proj == 'All projects':
        choice = st.sidebar.radio('Sort By:-', ['Date added', 'Due Date', 'Priority'])
        if choice == 'Date added':
            display = projects
        elif choice == 'Due Date':
            display = projects.sort_values(by='Due Date')
        else:
            display = projects.sort_values(by='Priority', ascending=False)

        if st.sidebar.checkbox('Hide Past Due'):
            projects['Due Date'] = pd.to_datetime(projects['Due Date']).dt.date
            display = projects[projects['Due Date'] >= today]

        if st.sidebar.checkbox('Hide completed projects'):
            display = projects[projects['Completed'] == 0]
        names, date, priorities, completed = st.columns(4)
        with names:
            st.markdown('**Name**')
            for i in display['Name']:
                st.write(i)
                st.write('----')
        with date:
            st.markdown('**Due Date**')
            # noinspection PyBroadException
            try:
                for i, j, k, p in zip(display['day'], display['month'], display['year'], display['Due Date']):
                    if p < today:
                        st.write('Past due')
                    elif p == today:
                        st.write('Due today')
                    else:
                        st.write(str(i), str(j), str(k))
                    st.write('----')
            except Exception as e:
                pass
        with priorities:
            st.markdown('**Priority**')
            for i in display['Priority']:
                st.write(str(i))
                st.write('----')
        with completed:
            st.markdown('**Completed Tasks**')
            for comp, total in zip(display['Completed Tasks'], display['Total Tasks']):
                st.write(f'{comp}/{total}')
                st.write('----')

    # Managing a project:
    # Make separate dataframes for tasks and details or add task columns after details

    else:
        # noinspection PyBroadException

        try:
            proj_row = projects[projects['Name'] == proj]
            proj_descr = (proj_row['descr'].values[0])
            st.markdown(f'<h2 style="font-weight: bolder;text-decoration-line: underline; ">{proj}</h2>',
                        unsafe_allow_html=True)
            st.markdown(f'<h4>{proj_descr}</h4>', unsafe_allow_html=True)

            proj_data = pd.read_excel(f'projects_{proj}.xlsx')
            proj_data = helper.clean_df(proj_data)

            # Manage tasks inside a project
            with st.expander("Manage tasks: "):
                proj_tasks, status, functions = st.columns(3)

                with functions:
                    # add task
                    task_title = st.text_input('Task title')
                    if st.button('Add task'):
                        if task_title in list(proj_data['Task']):
                            st.error('Task already exists')
                        elif task_title == '':
                            task_title = f'Task {len(proj_data["Task"])}'
                        else:
                            proj_data = helper.clean_df(proj_data)
                            proj_data.loc[len(proj_data.index)] = [task_title, 0,0]
                            index = projects.index[projects['Name'] == proj].tolist()
                            projects.at[index[0], 'Total Tasks'] = projects.at[index[0], 'Total Tasks'] + 1

                    projects.to_excel('projects.xlsx')
                    proj_data.to_excel(f'projects_{proj}.xlsx')
                    st.write('---')

                    # delete task
                    temp_list = list(proj_data['Task'])
                    temp_list.insert(0, 'Delete')
                    selected_task = st.selectbox('select a task', temp_list)
                    if st.button('Delete task permanently'):
                        proj_data.drop(proj_data.index[(proj_data["Task"] == selected_task)], axis=0, inplace=True)
                        projects.to_excel('projects.xlsx')
                        proj_data.to_excel(f'projects_{proj}.xlsx')
                        index = projects.index[projects['Name'] == proj].tolist()
                        projects.at[index[0], 'Total Tasks'] = projects.at[index[0], 'Total Tasks'] - 1
                    projects.to_excel('projects.xlsx')
                    proj_data.to_excel(f'projects_{proj}.xlsx')

                with proj_tasks:
                    proj_data = pd.read_excel(f'projects_{proj}.xlsx')
                    proj_data = helper.clean_df(proj_data)
                    if proj_data.shape[0] == 0:
                        st.write('No tasks yet')
                    else:
                        helper.completed_tasks(proj_data)
                        tasks_completed = helper.completed_tasks(proj_data)
                        index = projects.index[projects['Name'] == proj].tolist()
                        projects.at[index[0], 'Completed Tasks'] = tasks_completed
                        projects.to_excel('projects.xlsx')
                        proj_data.to_excel(f'projects_{proj}.xlsx')
            projects.to_excel('projects.xlsx')
            proj_data.to_excel(f'projects_{proj}.xlsx')
            # Status of completion

            project_completion = dsf.project_completion(proj_data)
            index = projects.index[projects['Name'] == proj].tolist()
            if project_completion == True:
                projects.at[index[0], 'Completed'] = 1

            else:
                projects.at[index[0], 'Completed'] = 0
            with st.expander('Delete the whole project'):

                if st.button('Delete project permanently'):

                    dsf.progress()
                    st.write("Project has been deleted successfully,head back to your projects")
                    projects.drop(projects.loc[projects['Name'] == proj].index, inplace=True)
                    os.remove(f'projects_{proj}.xlsx')

            projects.to_excel('projects.xlsx')

        except Exception as e:
            e
        dates = helper.get_dates(projects)

        st.dataframe(dates)
        project_page_completed = True
