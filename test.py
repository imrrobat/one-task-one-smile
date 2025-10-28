from nicegui import ui 

with ui.row().classes('w-full').style('border:1px solid;height:100vh;'):
    ui.column().style('border:1px solid;flex:1;height:100vh;')
    
    ui.column().style('border:1px solid;flex:4;height:100vh;')

ui.run()