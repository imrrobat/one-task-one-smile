from nicegui import ui 
import jdatetime as jdt
from utils import load_tasks,add_task


ui.add_head_html('''
<link href="https://cdn.jsdelivr.net/npm/vazir-font@30.1.0/dist/font-face.css" rel="stylesheet" type="text/css" />

<style>
body, .q-layout, .q-page-container, .q-page {
    direction: rtl !important;
    text-align: right !important;
    font-family: Vazir, sans-serif !important; 
}


.q-btn, .q-input, .q-field__native, .q-table, .q-card, .q-toolbar {
    font-family: Vazir, sans-serif !important;
}
</style>
''')

ui.colors(asli="#ED775A",ghermez="#E62727",sabz="#08CB00")
# ui.dark_mode(True)


def submit_task():
    if category.value == cats[0]:
        add_task(new_task.value, priority.value, 'work')
    elif category.value == cats[1]:
        add_task(new_task.value, priority.value, 'life')
    elif category.value == cats[2]:
        add_task(new_task.value, priority.value, 'fun')

    new_task.value = ""
    priority.value = 5
    category.value = cats[0]
    
    task_view.refresh()
 
def done_a_task(title):
    now = jdt.datetime.now()
    date = f'{now.year}-{now.month}-{now.day}'
    print(title)   
    
with ui.row().style('width: 100%; height: 100vh;'):
    # dashboard
    with ui.column().style('flex: 1; padding: 16px; border: 1px solid #ddd;').classes('h-full'):
        ui.label('وضعیت کلی').style('font-weight:bold;')
        ui.label('تعداد کل لبخندها')
        ui.label('لبخندهای این ماه')
        ui.label('لبخندهای امروز')
        
        ui.separator()
        ui.label('افزودن تسک').style('font-weight:bold;')
        new_task = ui.input('عنوان تسک').classes('w-full').props('dense outlined')
        
        cats = ['کار', 'رشد فردی و زندگی','تفریح و استراحت']
        category = ui.select(cats,value=cats[0]).classes('w-full')
        
        # slider = ui.slider(min=0, max=10, value=5,step=1, on_change=lambda e:ui.notify(f'اهمیت {e.value}/10',type='info'))
        priority = ui.slider(min=1, max=10, value=5,step=1).props('color=asli')
        with ui.row().classes('w-full justify-center gap-1'):
            ui.label('اهمیت:')
            ui.label().bind_text_from(priority,'value')
        ui.button(text="ثبت کار",on_click=submit_task).classes('w-full').props('color=asli')
        
    
    #task view
    with ui.column().style('flex: 4; border: 1px solid #ddd; padding: 16px;').classes('h-full'):
        with ui.row().classes('w-full gap-4'):
            
            @ui.refreshable
            def task_view():
                all_tasks = load_tasks()
                
                # work
                with ui.card().props('flat').style('flex: 1.2;border: 1px solid #ddd; display: flex; flex-direction: column; justify-content: center; padding: 16px;'):
                    ui.label('کار').style('font-weight:bold;')
                    
                    with ui.scroll_area().props('dense padding-20'):
                        work_tasks = [task for task in all_tasks if task['category']=='work']
                        for task in work_tasks:
                            with ui.row().classes('gap-2'):
                                title = ui.label(task['title'])
                                ui.button(icon='done',on_click=lambda e,title=title:done_a_task(title.text)).props('dense color=sabz size=xs')
                                ui.button(icon='remove').props('dense color=ghermez size=xs')
                
                # lifestyle              
                with ui.card().props('flat').style('flex: 1;border: 1px solid #ddd; display: flex; flex-direction: column; justify-content: center; padding: 16px;'):
                    ui.label('زندگی و رشد فردی').style('font-weight:bold;')
                    
                    
                    with ui.scroll_area().props('dense padding-20'):
                        life_tasks = [task for task in all_tasks if task['category']=='life']
                        for task in life_tasks:
                            with ui.row().classes('gap-2'):
                                title = ui.label(task['title'])
                                ui.button(icon='done',on_click=lambda e,title=title:done_a_task(title.text)).props('dense color=sabz size=xs')
                                ui.button(icon='remove').props('dense color=ghermez size=xs')
                                
                
                #fun 
                with ui.card().props('flat').style('flex: 0.9;border: 1px solid #ddd; display: flex; flex-direction: column; justify-content: center; padding: 16px;'):
                    ui.label('تفریح و استراحت').style('font-weight:bold;')
                    
                    
                    with ui.scroll_area().props('dense'):
                        fun_tasks = [task for task in all_tasks if task['category']=='fun']
                        for task in fun_tasks:
                            with ui.row().classes('gap-2'):
                                title = ui.label(task['title'])
                                ui.button(icon='done',on_click=lambda e,title=title:done_a_task(title.text)).props('dense color=sabz size=xs')
                                ui.button(icon='remove').props('dense color=ghermez size=xs')

            task_view()                   

ui.run(title='OTOS')
