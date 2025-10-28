from nicegui import ui
from snip import farsi_rtl
import jdatetime as jdt
from utils import today_log

dark_on = False
def stat():
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

    last_10_days = []
    stat = {}
    
    ui.markdown('###آمار 10 روز قبل')
    
    for i in range(10):
        day = today - jdt.timedelta(days=i)
        day_str = f'{day.year}-{day.month:02d}-{day.day:02d}'
        last_10_days.append(day_str)
    
    with ui.row().classes('w-full').style('align-items: stretch; height: 100%;'):
        with ui.column().classes('p-2').style('flex:1;border:1px solid;border-radius:5px;'):
            for day in last_10_days:
                day_log = today_log(day)
                smile_count = sum(int(item['priority']) for item in day_log)
                ui.label(f'روز {day} - لبخندها {smile_count}')
                
                stat[day] = smile_count
        with ui.column().style('flex:4;border:1px solid;border-radius:5px;'):
            ui.echart({
                'xAxis': {
                    'type': 'category',
                    'data': list(stat.keys()),
                    'axisLabel': {'rotate': 45},
                },
                'yAxis': {'type': 'value'},
                'tooltip': {'trigger': 'axis'},
                'grid': {'bottom': 70, 'left': 50, 'right': 20, 'top': 40},
                'series': [
                    {
                        'data': list(stat.values()),
                        'type': 'bar',
                        'itemStyle': {'color': "#A434BB"},
                        'barWidth': '30%',
                    },
                    {
                        'data': list(stat.values()),
                        'type': 'line',
                        'symbol': 'circle',
                        'symbolSize': 8,
                        'lineStyle': {'color': "#4CAF50", 'width': 2},
                        'itemStyle': {'color': "#DA7E14"},
                        'smooth': True, 
                    },
                ],
            }).style('align-items: stretch; height: 100%;')
            
    
    
    ui.link('بازگشت به صفحه اصلی','/').classes(
    'q-btn q-btn-item non-selectable no-outline q-btn--flat q-btn--rectangle bg-purple text-white'
) 