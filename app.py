from nicegui import ui 
import jdatetime as jdt
from utils import load_tasks,add_task,get_task,delete_task
from utils import mark_task_done,update_data
from utils import load_data_file,summary_info
from utils import today_log,get_rank
from snip import farsi_rtl,no_scroll

dark_on = False

ui.add_head_html(no_scroll)
ui.add_head_html(farsi_rtl)

ui.colors(asli="#36BA98",ghermez="#E62727",sabz="#08CB00",purple="#9112BC",yellow="#FFD93D")

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
).props('color=purple')

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
    date = f'{now.year}-{now.month:02d}-{now.day:02d}'
    
    currnet_task = get_task(title)
    update_data(int(currnet_task['priority']), 1)
    
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
     
with ui.row().style('width: 100%; height: 100vh;'):
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
                ui.label(f'کل تسک ها: {info['count_tasks']}')
                
            ui.label(f'تعداد کل لبخندها: {summary['total']}')
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
        
        ui.link('پیشرفت روز', 'http://127.0.0.1:8083/today').classes(
    'q-btn q-btn-item non-selectable no-outline q-btn--flat q-btn--rectangle bg-purple text-white'
)             
        ui.link('مشاهده آمار', 'http://127.0.0.1:8083/stat').classes(
    'q-btn q-btn-item non-selectable no-outline q-btn--flat q-btn--rectangle bg-yellow text-black'
)                 


@ui.page('/today')
def today():
    ui.add_head_html(farsi_rtl)

    ui.colors(asli="#36BA98",ghermez="#E62727",sabz="#08CB00",purple="#9112BC",yellow="#FFD93D")

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
    ).props('color=purple')

    today = jdt.datetime.now()
    day = f'{today.year}-{today.month:02d}-{today.day:02d}'
    log = today_log(day)
    
    count_smile = 0
    
    for item in log:
        count_smile += int(item['priority'])
    
    yesterday = today - jdt.timedelta(days=1)
    yesterday_str = f'{yesterday.year}-{yesterday.month:02d}-{yesterday.day:02d}'
    
    yesterday_log = today_log(yesterday_str)
    count_smile_yesterday = 0
    
    for item in yesterday_log:
        count_smile_yesterday += int(item['priority'])
    
    change_percent = (count_smile - count_smile_yesterday) / count_smile_yesterday * 100
    

    
    with ui.row():
        ui.label(f'گزارش امروز {today.year}/{today.month}/{today.day}').style('font-weight:bold;')
        ui.label(f'لبخندهای کسب شده: {count_smile}').style('font-weight:bold;')
        
        if change_percent > 0:
            ui.label(f"امروز نسبت به دیروز {change_percent:.1f}% بهتر بودی").style('font-weight:bold; color:#08CB00;')
        elif change_percent < 0:
            ui.label(f"امروز نسبت به دیروز {abs(change_percent):.1f}% بدتر بودی").style('font-weight:bold; color:#E62727;')
        else:
            ui.label("هیچ تغییری نسبت به دیروز نداشتی").style('font-weight:bold;')
    
    with ui.row().style('width: 100%; gap: 8px;'):
        with ui.column().style('flex: 1; border: 1px solid #ccc; padding: 8px;'):
            work_today = [item for item in log if item['category']=='work']
            ui.label('کار').style('font-weight:bold;')
            ui.separator()
            if work_today:
                for item in work_today:
                    ui.label(f'✅ {item['title']}')
            else:
                ui.label(f'امروز کاری انجام نشده 💔')
                
        with ui.column().style('flex: 1; border: 1px solid #ccc; padding: 8px;'):
            life_today = [item for item in log if item['category']=='life']
            ui.label('زندگی و رشد فردی').style('font-weight:bold;')
            ui.separator()
            if life_today:
                for item in life_today:
                    ui.label(f'✅ {item['title']}')
            else:
                ui.label(f'امروز رشد فردی نداشتیم 💔')
            
                
        with ui.column().style('flex: 1; border: 1px solid #ccc; padding: 8px;'):
            fun_today = [item for item in log if item['category']=='fun']
            ui.label('استراحت و تفریح').style('font-weight:bold;')
            ui.separator()
            if fun_today:
                for item in fun_today:
                    ui.label(f'✅ {item['title']}')
            else:
                ui.label(f'امروز تفریحی انجام نشده 💔')
    ui.link('بازگشت به صفحه اصلی','http://127.0.0.1:8083/').classes(
    'q-btn q-btn-item non-selectable no-outline q-btn--flat q-btn--rectangle bg-purple text-white'
) 

@ui.page('/stat')
def stat():
    ui.add_head_html(farsi_rtl)
    ui.colors(asli="#36BA98",ghermez="#E62727",sabz="#08CB00",purple="#9112BC",yellow="#FFD93D")

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
    ).props('color=purple')

    ui.markdown('###آمار 10 روز قبل')
    
    today = jdt.datetime.now()

    last_10_days = []
    
    for i in range(10):
        day = today - jdt.timedelta(days=i)
        day_str = f'{day.year}-{day.month:02d}-{day.day:02d}'
        last_10_days.append(day_str)
    
    for day in last_10_days:
        day_log = today_log(day)
        smile_count = sum(int(item['priority']) for item in day_log)
        ui.label(f'روز {day} - لبخندها {smile_count}')

    
    ui.link('بازگشت به صفحه اصلی','http://127.0.0.1:8083/').classes(
    'q-btn q-btn-item non-selectable no-outline q-btn--flat q-btn--rectangle bg-purple text-white'
) 
             
ui.run(title='OTOS',port=8083, favicon='otos.png')
