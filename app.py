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

ui.colors(asli="#972E2E")

with ui.row().style('width: 100%; height: 100vh;'):
    # dashboard
    with ui.column().style('flex: 1; padding: 16px; border: 1px solid #ddd;'):
        ui.label('وضعیت کلی')
        ui.separator()
        ui.input('عنوان تسک').classes('w-full').props('dense outlined')
        
        cats = ['کار', 'رشد فردی و زندگی','تفریح و استراحت']
        category = ui.select(cats,value=cats[0]).classes('w-full')
        
        # slider = ui.slider(min=0, max=10, value=5,step=1, on_change=lambda e:ui.notify(f'اهمیت {e.value}/10',type='info'))
        slider = ui.slider(min=1, max=10, value=5,step=1).props('color=asli')
        with ui.row().classes('w-full justify-center gap-1'):
            ui.label('اهمیت:')
            ui.label().bind_text_from(slider,'value')
        ui.button(text="ثبت کار").classes('w-full').props('color=asli')
        
    
    #task view
    with ui.column().style('flex: 4; border: 1px solid #ddd; padding: 16px;'):
        with ui.row().classes('w-full gap-4'):  # ردیف کارت‌ها
            with ui.card().props('flat').style('flex: 1;border: 1px solid #ddd; display: flex; flex-direction: column; justify-content: center; padding: 16px;'):
                ui.label('کارت')
                ui.label('توضیحات کارت...')
            with ui.card().props('flat').style('flex: 1;border: 1px solid #ddd; display: flex; flex-direction: column; justify-content: center; padding: 16px;'):
                ui.label('کارت')
                ui.label('توضیحات کارت...')
            with ui.card().props('flat').style('flex: 1;border: 1px solid #ddd; display: flex; flex-direction: column; justify-content: center; padding: 16px;'):
                ui.label('کارت')
                ui.label('توضیحات کارت...')

                    

        
    

ui.run(title='OTOS')
