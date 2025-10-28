from nicegui import ui
from snip import farsi_rtl
import jdatetime as jdt
from utils import today_log

dark_on = False

def today():
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
    
    try:
        change_percent = (count_smile - count_smile_yesterday) / count_smile_yesterday * 100
    except Exception:
        change_percent = 0 
    

    
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
    ui.link('بازگشت به صفحه اصلی','/').classes(
    'q-btn q-btn-item non-selectable no-outline q-btn--flat q-btn--rectangle bg-purple text-white'
) 