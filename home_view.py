from nicegui import ui
from snip import farsi_rtl, no_scroll
import jdatetime as jdt
import csv,os
from utils import load_tasks,add_task,get_task,delete_task
from utils import mark_task_done,update_data
from utils import load_data_file,summary_info
from utils import get_rank

dark_on = False

def home():

    ui.add_head_html(no_scroll)
    ui.add_head_html(farsi_rtl)
    
    ui.colors(
        asli="#BE1D1D",
        ghermez="#E62727",
        sabz="#08CB00",
        purple="#9112BC",
        yellow="#FFD93D"
    )

    def toggle_dark():
        global dark_on
        if dark_on:
            ui.dark_mode(False)
            dark_on = False
            toggle_btn.props('color=purple').classes(remove='text-black', add='text-white')
        else:
            ui.dark_mode(True)
            dark_on = True
            toggle_btn.props('color=yellow').classes(remove='text-white', add='text-black')

    toggle_btn = ui.button(icon='bedtime', on_click=toggle_dark).classes(
        'fixed bottom-4 left-4 text-white'
    ).props('color=purple round')

    
    def init_tasks(file_path='tasks.csv'): 
        
        if not os.path.exists(file_path):
            print(f"⚠️ File '{file_path}' not found. Skipped cleaning.")
            return
        
        new_rows = []
        today = jdt.date.today()
        removed_count = 0

        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    task_date = jdt.date.fromisoformat(row['date'])
                except Exception as e:
                    print(f"⚠️ Error in Date : {row['date']}: {e}")
                    continue

                days_passed = (today - task_date).days

                if days_passed > 10:
                    if row['is_done'].lower() == 'true':
                        print(f"🧹 Deleted (and Done) : {row['title']}")
                    else:
                        print(f"⚠️ Deleted (not Done) : {row['title']}")
                        update_data(-100, 0)
                    removed_count += 1
                else:
                    new_rows.append(row)

        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id','title','category','priority','date','is_done','done_date'])
            writer.writeheader()
            writer.writerows(new_rows)

        print(f"\n✅ Clean Tasks... {removed_count} Task Deleted...")
    
    init_tasks()
    
    def submit_task():
        now = jdt.datetime.now()
        date = f'{now.year}-{now.month:02d}-{now.day:02d}'
        
        if category.value == cats[0]:
            add_task(new_task.value, priority.value, 'work', date)
        elif category.value == cats[1]:
            add_task(new_task.value, priority.value, 'life', date)
        elif category.value == cats[2]:
            add_task(new_task.value, priority.value, 'fun', date)

        new_task.value = ""
        priority.value = 5
        category.value = cats[0]
        
        task_view.refresh()
    
    def done_a_task(title):
        now = jdt.datetime.now()
        date = f'{now.year}-{now.month:02d}-{now.day:02d}'
        
        currnet_task = get_task(title)
        update_data(int(currnet_task['priority']),1)
        
        mark_task_done(title,date) 
        task_view.refresh()  
        info_view.refresh()
    
    def remove_a_task(title):
        print(get_task(title)) 
        currnet_task = get_task(title)
        update_data(int(currnet_task['priority'])*-1, 0)
        
        delete_task(title)
        
        task_view.refresh()
        info_view.refresh()
        
    with ui.row().classes('w-full').style('height:100vh;'):
        # dashboard
        with ui.column().style('flex: 1; padding: 16px; border: 1px solid #ddd;').classes('h-full'):
            @ui.refreshable
            def info_view():
                today = jdt.datetime.now()
                info = load_data_file()
                summary = summary_info()
                
                with ui.row().classes('gap-1'):
                    rank = get_rank(info['score'])
                    ui.label(f'سلام {rank}').style('font-weight:bold;')
                    ui.label(f'امروز: {today.year}/{today.month}/{today.day}').style('font-weight:bold;')
                    
                ui.separator()
                with ui.row().classes('gap-1'):
                    ui.label('وضعیت کلی:').style('font-weight:bold;')
                    ui.label(f'امتیاز: {info['score']} |')
                    ui.label(f'تسک ها: {info['count_tasks']}')
                    
                ui.label(f'لبخندهای این ماه: {summary['month_total']}')
                ui.label(f'لبخندهای امروز: {summary['today_total']}')
            info_view()
            
            ui.separator()
            ui.label('افزودن تسک').style('font-weight:bold;').props('required')
            new_task = ui.input('عنوان تسک').classes('w-full').props('dense outlined')
            
            cats = ['کار', 'رشد فردی و زندگی','تفریح و استراحت']
            category = ui.select(cats,value=cats[0]).classes('w-full')
            
            # slider = ui.slider(min=0, max=10, value=5,step=1, on_change=lambda e:ui.notify(f'اهمیت {e.value}/10',type='info'))
            priority = ui.slider(min=1, max=10, value=5,step=1).props('color=asli')
            with ui.row().classes('w-full justify-center gap-1'):
                ui.label('اهمیت:')
                ui.label().bind_text_from(priority,'value')
            ui.button(text="ثبت کار",on_click=submit_task).classes('w-full').props('color=asli')
            ui.button(text="اینو کی ساخته؟",on_click=lambda e:ui.notify("علی حیدری (آقای ربات)"))\
                .classes('w-full')\
                .props('color=green-3')
            
            
        
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
                                    ui.button(icon='remove',on_click=lambda e,title=title:remove_a_task(title.text)).props('dense color=ghermez size=xs')
                    
                    # lifestyle              
                    with ui.card().props('flat').style('flex: 1;border: 1px solid #ddd; display: flex; flex-direction: column; justify-content: center; padding: 16px;'):
                        ui.label('زندگی و رشد فردی').style('font-weight:bold;')
                
                        with ui.scroll_area().props('dense padding-20'):
                            life_tasks = [task for task in all_tasks if task['category']=='life']
                            for task in life_tasks:
                                with ui.row().classes('gap-2'):
                                    title = ui.label(task['title'])
                                    ui.button(icon='done',on_click=lambda e,title=title:done_a_task(title.text)).props('dense color=sabz size=xs')
                                    ui.button(icon='remove',on_click=lambda e,title=title:remove_a_task(title.text)).props('dense color=ghermez size=xs')
                                    
                    
                    #fun 
                    with ui.card().props('flat').style('flex: 0.9;border: 1px solid #ddd; display: flex; flex-direction: column; justify-content: center; padding: 16px;'):
                        ui.label('تفریح و استراحت').style('font-weight:bold;')
                        
                        with ui.scroll_area().props('dense'):
                            fun_tasks = [task for task in all_tasks if task['category']=='fun']
                            for task in fun_tasks:
                                with ui.row().classes('gap-2'):
                                    title = ui.label(task['title'])
                                    ui.button(icon='done',on_click=lambda e,title=title:done_a_task(title.text)).props('dense color=sabz size=xs')
                                    ui.button(icon='remove',on_click=lambda e,title=title:remove_a_task(title.text)).props('dense color=ghermez size=xs')

                task_view() 
            
            ui.link('پیشرفت روز','/today').classes(
        'q-btn q-btn-item non-selectable no-outline q-btn--flat q-btn--rectangle bg-purple text-white'
        )             
            ui.link('مشاهده آمار', '/stat').classes(
        'q-btn q-btn-item non-selectable no-outline q-btn--flat q-btn--rectangle bg-yellow text-black'
        )                 
