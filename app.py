from nicegui import ui,native #,app

from home_view import home
from today_view import today
from yesterday_view import yesterday
from stat_view import stat

# app.native.window_args['maximized'] = True
app_port = native.find_open_port()

def root():
    ui.sub_pages(
        {
            '/':home,
            '/today': today,
            '/yesterday':yesterday,
            '/stat':stat
        }
    ).classes('w-full')




# ui.run(title='OTOS',port={app_port}, favicon='otos.png')
ui.run(
    root=root,
    title='OTOS',
    port=app_port,
    reload=False,
    # native=True
)
