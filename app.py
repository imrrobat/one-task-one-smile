from nicegui import ui 

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

with ui.row().style('width: 100%; height: 100vh;'):
    # dashboard
    with ui.column().style('flex: 1; padding: 16px;'):
        ui.label('➕ Add Task (1/3)')
    
    #task view
    with ui.column().style('flex: 2; border: 1px solid #ddd; padding: 16px;'):
        ui.label('📋 Task List (2/3)')
    

ui.run(title='OTOS')
