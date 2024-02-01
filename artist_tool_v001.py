import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.ticker as mticker
from st_aggrid import AgGrid, ColumnsAutoSizeMode
from st_aggrid.grid_options_builder import GridOptionsBuilder 

def get_shots_STATUS_count(proj_tasks):
    nys_cnt = 0
    nys_shot_name = list()
    wip_cnt = 0
    wip_shot_name = list()
    rej_cnt = 0
    rej_shot_name = list()
    rev_cnt = 0
    rev_shot_name = list()
    app_cnt = 0
    app_shot_name = list()
    pub_cnt = 0
    pub_shot_name = list()
    for task in proj_tasks:
        if task['STATUS'] == 'NYS':
            nys_cnt += 1
            nys_shot_name.append(task['TASK NAME'])
        if task['STATUS'] == 'WIP':
            wip_cnt += 1
            wip_shot_name.append(task['TASK NAME'])
        if task['STATUS'] == 'REJ':
            rej_cnt += 1
            rej_shot_name.append(task['TASK NAME'])
        if task['STATUS'] == 'REV':
            rev_cnt += 1
            rev_shot_name.append(task['TASK NAME'])
        if task['STATUS'] == 'APP':
            app_cnt += 1
            app_shot_name.append(task['TASK NAME'])
        if task['STATUS'] == 'PUB':
            pub_cnt += 1
            pub_shot_name.append(task['TASK NAME'])
    return [nys_cnt, wip_cnt, rej_cnt, rev_cnt, app_cnt, pub_cnt], [(',').join(nys_shot_name), (',').join(wip_shot_name), (',').join(rej_shot_name), (',').join(rev_shot_name), (',').join(app_shot_name), (',').join(pub_shot_name)]

def calculate_status_degree(shot_statuses, total_shots):
    status_percentages = list()
    status_list = list()

    if (shot_statuses[0] / total_shots) * 360 != 0:
        status_percentages.append((shot_statuses[0] / total_shots) * 360)
        status_list.append('NYS')
    if (shot_statuses[1] / total_shots) * 360 != 0:
        status_percentages.append((shot_statuses[1] / total_shots) * 360)
        status_list.append('WIP')
    if (shot_statuses[2] / total_shots) * 360 != 0:
        status_percentages.append((shot_statuses[2] / total_shots) * 360)
        status_list.append('REJ')
    if (shot_statuses[3] / total_shots) * 360 != 0:
        status_percentages.append((shot_statuses[3] / total_shots) * 360)
        status_list.append('REV')
    if (shot_statuses[4] / total_shots) * 360 != 0:
        status_percentages.append((shot_statuses[4] / total_shots) * 360)
        status_list.append('APP')
    if (shot_statuses[5] / total_shots) * 360 != 0:
        status_percentages.append((shot_statuses[5] / total_shots) * 360)
        status_list.append('PUB')
    

    return status_percentages, status_list

def add_graph_labels(x, y, shot_names):
    for i in range(len(x)):
        plt.text(i, y[i], shot_names[i], ha= 'center')

# initial page-setup
st.set_page_config(page_title='Artist Tool', layout='wide')

# import external css
with open('./css/artist_tool_v001.css') as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

# heading 
st.markdown('<h1>Artist Tool : pushpendratiwari</h1>', unsafe_allow_html=True)

# template task list 
task_list = [
                {'proj_01' : [
                                {'TASK NAME': 'shot_01', 'STATUS': 'WIP', 'DAYS REMAINING': 1, 'START DATE': '01-01-2023', 'END DATE': '01-02-2023'},
                                {'TASK NAME': 'shot_02', 'STATUS': 'WIP', 'DAYS REMAINING': 1, 'START DATE': '01-01-2023', 'END DATE': '01-02-2023'},
                                {'TASK NAME': 'shot_03', 'STATUS': 'NYS', 'DAYS REMAINING': 1, 'START DATE': '01-01-2023', 'END DATE': '01-02-2023'},
                                {'TASK NAME': 'shot_04', 'STATUS': 'REJ', 'DAYS REMAINING': 1, 'START DATE': '01-01-2023', 'END DATE': '01-02-2023'},
                                {'TASK NAME': 'shot_05', 'STATUS': 'REV', 'DAYS REMAINING': 1, 'START DATE': '01-01-2023', 'END DATE': '01-02-2023'},
                                {'TASK NAME': 'shot_06', 'STATUS': 'REV', 'DAYS REMAINING': 1, 'START DATE': '01-01-2023', 'END DATE': '01-02-2023'},
                                {'TASK NAME': 'shot_07', 'STATUS': 'REV', 'DAYS REMAINING': 1, 'START DATE': '01-01-2023', 'END DATE': '01-02-2023'},
                                {'TASK NAME': 'shot_04a', 'STATUS': 'PUB', 'DAYS REMAINING': 1, 'START DATE': '01-01-2023', 'END DATE': '01-02-2023'}
                ]},
                {'proj_02' : [
                                {'TASK NAME': 'shot_01', 'STATUS': 'WIP', 'DAYS REMAINING': 1, 'START DATE': '01-01-2023', 'END DATE': '01-02-2023'},
                                {'TASK NAME': 'shot_02', 'STATUS': 'WIP', 'DAYS REMAINING': 1, 'START DATE': '01-01-2023', 'END DATE': '01-02-2023'},
                                {'TASK NAME': 'shot_13', 'STATUS': 'NYS', 'DAYS REMAINING': 1, 'START DATE': '01-01-2023', 'END DATE': '01-02-2023'},
                                {'TASK NAME': 'shot_23', 'STATUS': 'APP', 'DAYS REMAINING': 1, 'START DATE': '01-01-2023', 'END DATE': '01-02-2023'},
                                {'TASK NAME': 'shot_33', 'STATUS': 'PUB', 'DAYS REMAINING': 1, 'START DATE': '01-01-2023', 'END DATE': '01-02-2023'},
                                {'TASK NAME': 'shot_103', 'STATUS': 'NYS', 'DAYS REMAINING': 1, 'START DATE': '01-01-2023', 'END DATE': '01-02-2023'},
                                {'TASK NAME': 'shot_203', 'STATUS': 'NYS', 'DAYS REMAINING': 1, 'START DATE': '01-01-2023', 'END DATE': '01-02-2023'}
                ]},
                {'proj_03' : [
                                {'TASK NAME': 'shot_01', 'STATUS': 'WIP', 'DAYS REMAINING': 1, 'START DATE': '01-01-2023', 'END DATE': '01-02-2023'},
                                {'TASK NAME': 'shot_02', 'STATUS': 'WIP', 'DAYS REMAINING': 1, 'START DATE': '01-01-2023', 'END DATE': '01-02-2023'},
                                {'TASK NAME': 'shot_23', 'STATUS': 'APP', 'DAYS REMAINING': 1, 'START DATE': '01-01-2023', 'END DATE': '01-02-2023'},
                                {'TASK NAME': 'shot_33', 'STATUS': 'APP', 'DAYS REMAINING': 1, 'START DATE': '01-01-2023', 'END DATE': '01-02-2023'}
                ]}
                
]


# creating UI for all tasks
for tasks in task_list:
    for proj, proj_tasks in tasks.items():
        # creating expander for each project
        with st.expander(label=proj):
            # creating pandas dataframe
            df = pd.DataFrame(proj_tasks)

            # defining two columns for table and graph
            # col1, col2 = st.columns([0.7, 0.3])
            col1, col2, col3 = st.columns([0.5, 0.25, 0.25])

            # attaching a streamlit data_editor table to col1
            # col1.data_editor(df, key=proj, disabled=True)

            # attaching st_aggrid to col1
            with col1:
                options_builder = GridOptionsBuilder.from_dataframe(df)
                # options_builder.configure_column(field='Image URL', cellRenderer= render_image)
                options_builder.configure_selection(selection_mode="single", use_checkbox=True)
                options_builder.configure_grid_options(alwaysShowVerticalScroll=True, alwaysShowHorizontalScroll=True, enableRangeSelection=True, pagination=True)
                options_builder.configure_side_bar()

                grid_options = options_builder.build()
                # grid_options['rowHeight'] = 50
                # Create AgGrid component
                grid = AgGrid(df, 
                    gridOptions = grid_options,
                    allow_unsafe_jscode=True,
                    height=400, width=500, theme='material', 
                    enable_enterprise_modules=True,
                    columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)
            

            # attaching comment history to col2
            col2.write('huhuhuhuhuhuhuhuhu')
            
            # attaching option for graph type to col3
            graph_type = col3.selectbox(label='Select graph type : ', 
                                        options=['Bar Chart', 'Scatter Chart', 'Pie Chart'],
                                        placeholder='Choose an Option',
                                        key=proj)
            
            # attaching matplotlib graph to col2
            statuses_x_axis = ['NYS', 'WIP', 'REJ', 'REV', 'APP', 'PUB']
            shots_status_cnt_y_axis, shot_names = get_shots_STATUS_count(proj_tasks)

            if graph_type == 'Bar Chart':
                bar_color = ['red', 'yellow', 'black', 'blue', 'orange']
                
                figure = plt.figure()
                plt.xlabel('Statuses', fontsize=15)
                plt.ylabel('Shot Count', fontsize=15)
                plt.title('Statuses:Shot-Count Chart', fontsize=15)
                plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))
                plt.gca().yaxis.set_major_locator(mticker.MultipleLocator(1))
                plt.grid()
                # plt.bar(statuses_x_axis, shots_status_cnt_y_axis, width=0.2, color= bar_color)
                # plt.bar(statuses_x_axis, shots_status_cnt_y_axis, width= 0.2, color= bar_color, edgecolor= 'black', linewidth= 2, linestyle= '--', alpha= 0.5)
                
                plt.bar(statuses_x_axis, shots_status_cnt_y_axis, width=0.2, color= bar_color, alpha= 0.5)
                add_graph_labels(statuses_x_axis, shots_status_cnt_y_axis, shot_names)
                col3.write(figure)
            elif graph_type == 'Scatter Chart':
                figure = plt.figure()
                plt.xlabel('Statuses', fontsize=15)
                plt.ylabel('Shot Count', fontsize=15)
                plt.title('Statuses:Shot-Count Chart', fontsize=15)
                plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))
                plt.gca().yaxis.set_major_locator(mticker.MultipleLocator(1))
                plt.grid()

                # plt.scatter(statuses_x_axis, shots_status_cnt_y_axis, c='r', s=200, alpha=0.5, marker='*', linewidths=1, edgecolors='b')
                color = [30, 90, 70, 66, 99, 20]
                plt.scatter(statuses_x_axis, shots_status_cnt_y_axis, c=color, s=200, cmap='BrBG')
                cb = plt.colorbar()
                cb.set_label('Color Bar')
                add_graph_labels(statuses_x_axis, shots_status_cnt_y_axis, shot_names)
                col3.write(figure)
            elif graph_type == 'Pie Chart':
                status_degrees, status_list = calculate_status_degree(shots_status_cnt_y_axis, len(proj_tasks))
                figure = plt.figure()
                plt.title('Statuses:Shot-Count Chart', fontsize=15)
                i = 0
                label = list()
                for shot_name in shot_names:
                    if len(shot_name):
                        label.append(status_list[i] + ': ' + shot_name)
                        i += 1 
                plt.pie(x=status_degrees, labels=label) 
                plt.legend()
                
                col3.write(figure)


