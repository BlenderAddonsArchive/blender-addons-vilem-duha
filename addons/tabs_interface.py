
bl_info = {
    "name": "Tabs interface",
    "author": "Vilem Duha",
    "version": (1, 0),
    "blender": (2, 78, 0),
    "location": "Everywhere(almost)",
    "description": "Blender tabbed.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "All"}

import bpy,os

import bpy, bpy_types
from bpy.app.handlers import persistent

_hidden_panels = {}
_panels = {}
_context_items = []
_bl_panel_types = []
_pinned_panels = []
_tab_panels = {}
def hide_panel(tp_name):
    if tp_name in _hidden_panels:
        pass

    elif hasattr(bpy.types, tp_name):
        tp = getattr(bpy.types, tp_name)
        bpy.utils.unregister_class(tp)
        _hidden_panels[tp_name] = tp


def unhide_panel(tp_name):
    if tp_name in _hidden_panels:
       
        bpy.utils.register_class(_hidden_panels[tp_name])
        del _hidden_panels[tp_name]

    else:
        pass

DEFAULT_PANEL_PROPS = ['__class__', '__contains__', '__delattr__', '__delitem__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', '__weakref__', '_dyn_ui_initialize', 'append', 'as_pointer', 'bl_category', 'bl_context', 'bl_description', 'bl_idname', 'bl_label', 'bl_options', 'bl_region_type', 'bl_rna', 'bl_space_type', 'COMPAT_ENGINES', 'draw','draw_header', 'driver_add', 'driver_remove', 'get', 'id_data', 'is_property_hidden', 'is_property_readonly', 'is_property_set', 'items', 'keyframe_delete', 'keyframe_insert', 'keys', 'orig_category', 'path_from_id', 'path_resolve', 'poll', 'prepend', 'property_unset', 'remove', 'type_recast', 'values']

NOCOPY_PANEL_PROPS = ['__class__', '__contains__', '__delattr__', '__delitem__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', '__weakref__', '_dyn_ui_initialize', 'append', 'as_pointer', 'bl_category', 'bl_context', 'bl_description', 'bl_idname', 'bl_label', 'bl_options', 'bl_region_type', 'bl_rna', 'bl_space_type', 'COMPAT_ENGINES',  'driver_add', 'driver_remove', 'get', 'id_data', 'is_property_hidden', 'is_property_readonly', 'is_property_set', 'items', 'keyframe_delete', 'keyframe_insert', 'keys',  'orig_category', 'path_from_id', 'path_resolve', 'poll', 'prepend', 'property_unset', 'remove', 'type_recast', 'values']

class tabSetups(bpy.types.PropertyGroup):
    '''stores data for tabs'''
    tabsenum = bpy.props.EnumProperty(name='Post processor',
        items=[('tabID', 'tabb', 'tabbiiiieeee')])
    active_tab = bpy.props.StringProperty(name="Active tab", default="Machine")
    active_category = bpy.props.StringProperty(name="Active category", default="Machine")
	#name = bpy.props.StringProperty(name="Machine Name", default="Machine")
#    pass;

def updatePin(self, context) :
    #print(self.name, ' update pin')
    p=bpy.types.Scene.panelIDs[self.name]
    if self.pin:
        if p not in _pinned_panels:
            _pinned_panels.append(p)
    elif p in _pinned_panels:
        _pinned_panels.remove(p)
            

class panelData(bpy.types.PropertyGroup):
    '''stores data for panels'''
    
    #id = bpy.props.StringProperty(name="panel id", default="")
    pin = bpy.props.BoolProperty(name="pin", default=False, update = updatePin)
    
	
def getWTabCount(context):
    w = context.region.width
    wtabcount = int(w/110)
    if wtabcount == 0:
        wtabcount = 1
    return wtabcount
def getlabel(panel):
    return panel.bl_label
''''
@classmethod
def nopoll(cls, context):
    return False

@classmethod
def yespoll(cls, context):
    return True
  '''  
DONT_USE = [ 'DATA_PT_modifiers', 'OBJECT_PT_constraints', 'BONE_PT_constraints']   
def getPanelIDs():
    
    panelIDs = {}
    panel_tp = bpy.types.Panel
    for tp_name in dir(bpy.types):
        if tp_name.find('_tabs')==-1  or tp_name not in DONT_USE: #and tp_name.find('NODE_PT_category_')==-1
            tp = getattr(bpy.types, tp_name)
            #print(tp)
            if tp == panel_tp or not issubclass(tp, panel_tp):
                continue
                
            if (hasattr(tp, 'bl_options') and 'HIDE_HEADER' in tp.bl_options):
                print(tp.bl_rna.identifier)
            if not (hasattr(tp, 'bl_options') and 'HIDE_HEADER' in tp.bl_options):
                panelIDs[tp.bl_rna.identifier] = tp
                if tp.is_registered!=True:
                    print('not registered', tp.bl_label)
           
    #print(tp)
    return panelIDs
   
class myPanel:
    pass
    
'''
DATA_PT_modifiers.draw = modifiersDraw
    bpy.types.OBJECT_PT_constraints.draw = constraintsDraw
    bpy.types.BONE_PT_constraints.draw = 
'''

def buildTabDir():
    spaces={}
    newclasses = ()
    print('called buildtabdir')
    for pname in bpy.types.Scene.panelIDs:
        panel = bpy.types.Scene.panelIDs[pname]
        #panel = p#eval('bpy.types.'+p)
        #print((panel.bl_label))
        if hasattr(panel, 'bl_space_type'):
            st = panel.bl_space_type
            if st!= 'USER_PREFERENCES':
                #print((st))
                if spaces.get(st) == None:
                    spaces[st] = {}#[panel]
                
                if hasattr(panel, 'bl_region_type'):
                    rt = panel.bl_region_type
                    #print(rt)
                    if spaces[st].get(rt)==None:
                        spaces[st][rt] = []
                #cat = ''
                if hasattr(panel, 'bl_category'):
                    if not hasattr(panel, 'orig_category'):
                        panel.orig_category = panel.bl_category
                    #cat ='bl_category = "%s"' % panel.bl_category
                    panel.bl_category = 'Tools'
               
                spaces[st][rt].append(panel)
                panel.realID = panel.bl_rna.identifier
                panel.save_rna = panel.bl_rna
                hide_panel(panel.realID)
                #try:
                    
                #    bpy.utils.unregister_class(eval('bpy_types.bpy_types.'+panel.bl_rna.identifier))
                    #print('haha')
                    #bpy.utils.register_class(eval('bpy_types.bpy_types.'+panel.bl_rna.identifier))
                #except:
                #    pass;
    for sname in spaces:
        space = spaces[sname]
        for rname in space:
            region = space[rname]
            region.sort(key = getlabel)
    
    return spaces 
     
def getPanels(getspace, getregion):
    if not hasattr(bpy.types.Scene, 'panelIDs'):# or random.random()<0.01:
        bpy.types.Scene.panels = getPanelIDs()
        #if not hasattr(bpy.types.Scene, 'panelSpaces'):
        bpy.types.Scene.panelSpaces = buildTabDir()
        #bpy.types.Scene.tabCollections = {}
    #if not hasattr(bpy.context.scene, 'panelData'):
    
            
    return bpy.types.Scene.panelSpaces[getspace][getregion]
        
def drawEnable(self,context):
    layout = self.layout
    row = layout.row()
    row.label('Enable:')
    
def layoutActive(self,context):
    layout = self.layout
    layout.active = True
    layout.enabled = True
    #layout.label('\n\n\n\n\n\n\n\n\n')
    #for a in range(0,90):
    #    r = layout.separator()
        
def layoutSeparator(self,context):
    layout = self.layout
    layout.separator()
    
class CarryLayout:
    def __init__(self, layout):
        self.layout = layout

def drawNone(self,context):
    pass;

def tabRow(layout, variable_width):
    tab_scale = 0.8
    row = layout.row(align = True)
    row.scale_y=tab_scale
    #row.scale_x =.1
    if variable_width:
        row.alignment = 'LEFT'
    return row
    
def drawTabs(self,context,plist, tabID):
    
    variable_width = bpy.context.user_preferences.addons["tabs_interface"].preferences.variable_width

    w = context.region.width
    width_letters = int(w/10)
    if width_letters == 0:
        width_letters = 1
    
    s = bpy.context.scene
    tabpanel_data = s.panelTabData.get(tabID)
    if tabpanel_data == None:
        
        tabpanel_data = s.panelTabData[tabID]
    wtabcount = getWTabCount(context)
    
    draw_panels = []    
    categories={}
    
   
    active_tab = tabpanel_data.active_tab
    hasactivetab = False
    
    for pp in _pinned_panels:
        if pp in plist:
        
            draw_panels.append(pp)
    
    for p in plist:
        if hasattr(p,'bl_category'):
            if categories.get(p.orig_category) == None:
                categories[p.orig_category] = [p]
            else:
                categories[p.orig_category].append(p)
        if  tabpanel_data.active_tab == p.realID:
            hasactivetab = True
        
    #if not hasactivetab and len(draw_panels) == 0:
    #    tabpanel_data.active_tab = plist[0].realID
    #print(wtabcount)
    
    ti = 0
    preview= None
    layout = self.layout
   
    totalwidth = 0
    
    if len(plist)>1 and len(categories)==0:#property windows
        
        col = layout.column(align = True)
        #col.scale_y=.5
        #col.alignment = 'LEFT'
        row=tabRow(col, variable_width)
       
        for p in plist:
                
            if p.bl_label!='Preview':
                #col1=row.column(align = True)
               # print(self.activetab , p.realID, p.bl_label, p.bl_context)
                #print(dir(p))
                totalwidth+= len(p.bl_label)
                if tabpanel_data.active_tab == p.realID:#p.realID:
                    if p not in _pinned_panels:
                        draw_panels.append(p)

                    op = row.operator("wm.activate_panel", text=p.bl_label , emboss = False)
                    
                else:
                    op = row.operator("wm.activate_panel", text=p.bl_label , emboss = True )
                op.panel_id=p.realID
                op.tabpanel_id=tabID
                ti+=1
                if (not variable_width and ti == wtabcount) or (variable_width and totalwidth>width_letters):
                    ti = 0
                    row=tabRow(col, variable_width)
                    
                    totalwidth = 0
                    
            else:
                preview = p
        for i in range(ti,wtabcount):
            col1=row.column(align = True)
    elif len(categories)>0: #EVIL TOOL PANELS!
        bpy.types.VIEW3D_MT_editor_menus.draw_collapsible(context, layout)
        col = layout.column(align = True)
        cnames = list(categories)
        cnames.sort()
        
        prepend = ''
        icon = 'NONE'
        for cname in cnames:
            category = categories[cname]
            box = col
            #box =col.box()
            #box.scale_y = 0.9
            row=tabRow(box, variable_width)
            #sep = col.separator()
            if len(category)>1:
                #col = layout.column(align = True)
                ti=1
                
                #row.scale_y = 0.5
                row.label(cname)
                totalwidth+= len(cname)
               # row=tabRow(box, variable_width)
               
                #prepend = cname+ '>>'
                #icon = 'ANTIALIASED'
                #icon = 'NONE'
            else:
                #col = layout.column(align = True)
                row.label(cname)
                #prepend = cname+' >> '
                #icon = 'ANTIALIASED'
                #col = layout.column(align = True)
            #row = col.row(align = True)
            
            for p in category:
                if p.bl_label!='Preview':
                    totalwidth+= len(p.bl_label)
                    if tabpanel_data.active_tab == p.realID:
                        if p not in _pinned_panels:
                            draw_panels.append(p)
                        op = row.operator("wm.activate_panel", text=prepend + p.bl_label , emboss = False, icon = icon)
                    else:
                        op = row.operator("wm.activate_panel", text=prepend + p.bl_label , emboss = True , icon = icon)
                    op.panel_id=p.realID
                    op.tabpanel_id=tabID
                    ti+=1
                    if (not variable_width and ti == wtabcount) or (variable_width and totalwidth>width_letters):
                        row=tabRow(col, variable_width)
                        ti = 0
                        totalwidth = 0
                    
                else:
                    preview = p  
                icon = 'NONE'
                prepend = ''
    elif len(plist)==1:
        p = plist[0]
        #print(dir(self))
        self.text = p.bl_label
        layout.label(p.bl_label)
        p.draw(self, context)
    layout.active = True
    if preview != None:
        preview.draw(self, context)
    return draw_panels
    
def drawPanels(self, context, draw_panels):
    layout = self.layout
    for drawPanel in draw_panels:
        
        #layout.separator()
        #if len(drawPanels)>1 or hasattr(drawPanel, "draw_header"):
        box = layout.box()
        #box.scale_x = 0.2
        box.scale_y =.8
        #print(layout.introspect())
        row = box.row()
        row.scale_y=.8
        if hasattr(drawPanel, "draw_header"):
            
            #self.layout = row
            fakeself = CarryLayout(row)
            drawPanel.draw_header(fakeself,context)
            #row.label('Enable ')
        row.label(drawPanel.bl_label)
        #for p in bpy.types.Scene.panelIDs:
        
        
        pd = bpy.context.scene.panelData[drawPanel.realID]
        if pd.pin: icon = 'PINNED'
        else: icon = 'UNPINNED'
        row.prop(bpy.context.scene.panelData[drawPanel.realID],'pin' , icon_only = True, icon=icon)
        if hasattr(drawPanel, "draw"):
            #self.layout = box
            #col = layout.column()
            #fakeself = CarryLayout(col)
            drawPanel.draw(self,context)
        #_pinned_panels
        layoutActive(self,context)
 
def pollTabs(panels, context):
    draw_plist = []
    for p in panels:
        #p = panelIDs[pname]
        #p = eval('bpy.types.'+panelID)
        polled = True
        
        
        
        if hasattr(p, "poll"):
            
            try:
                polled = p.poll(context)
            except:
                #print ("Unexpected error:", sys.exc_info()[0])
                pass;
                print('badly implemented poll', p.bl_label)
    
        if polled:
            draw_plist.append(p)     
    return draw_plist
           
        
def getFilteredTabs(self,context):        
     
    
    getspace = self.bl_space_type 
    getregion = self.bl_region_type 
    tab_panel_category = ''
    if hasattr(self, 'bl_category'):
        tab_panel_category = self.bl_category
    panellist = getPanels(getspace, getregion )
    
    tabpanel = self#eval('bpy.types.' + tabID)
    
    
    possible_tabs = []
    possible_tabs_wider = []
    categories = []
    for panel in panellist:
        
        if panel.bl_label!= '':# and panel.bl_label!= 'Influence' and panel.bl_label!= 'Mapping': #these were crashing. not anymore.
            polled = True
            
            #first  filter context and category before doing eval and getting actual panel object. still using  fo data.
            if hasattr(panel, 'bl_context'): 
                pctx = panel.bl_context.upper()
                if panel.bl_context == 'particle':
                    pctx = 'PARTICLES'
                
                if hasattr(context.space_data, 'context'):
                    if not pctx == context.space_data.context:
                        polled =False
                        pass
                elif hasattr(context, 'mode'):
                    #TOOLS NEED DIFFERENT APPROACH!!! THS IS JUST AN UGLY UGLY HACK....
                    if panel.bl_context == 'mesh_edit':
                        pctx = 'EDIT_MESH'
                    elif panel.bl_context == 'curve_edit':
                        pctx = 'EDIT_CURVE'
                    elif panel.bl_context == 'surface_edit':
                        pctx = 'EDIT_SURFACE'
                    elif panel.bl_context == 'text_edit':
                        pctx = 'EDIT_TEXT'
                    elif panel.bl_context == 'armature_edit':
                        pctx = 'EDIT_ARMATURE'
                    elif panel.bl_context == 'mball_edit':
                        pctx = 'EDIT_METABALL'
                    elif panel.bl_context == 'lattice_edit':
                        pctx = 'EDIT_LATTICE'
                    elif panel.bl_context == 'posemode':
                        pctx = 'POSE'
                    elif panel.bl_context == 'mesh_edit':
                        pctx = 'SCULPT'
                    elif panel.bl_context == 'weightpaint':
                        pctx = 'PAINT_WEIGHT'    
                    elif panel.bl_context == 'vertexpaint':
                        pctx = 'PAINT_VERTEX'
                    elif panel.bl_context == 'vertexpaint':
                        pctx = 'PAINT_TEXTURE'
                    elif panel.bl_context == 'objectmode':
                        pctx = 'OBJECT'
                    
                    if not pctx == context.mode:
                        polled =False
                        pass
                   # print((context.space_data.context))
            if polled:
                possible_tabs_wider.append(panel)
            if hasattr(panel, 'bl_category'): 
                if panel.bl_category != tab_panel_category:
                    polled = False
                
            if polled:
                possible_tabs.append(panel)
    draw_tabs_list = pollTabs(possible_tabs, context)
    self.tabcount = len(draw_tabs_list)
    #print(self.tabcount)
    bpy.types.Scene.panelTabInfo[self.bl_idname] = [self.tabcount, possible_tabs_wider]
    for p in draw_tabs_list:# these are various functions defined all around blender for panels. We need them to draw the panel inside the tab panel
        for var in dir(p):
            if var not in DEFAULT_PANEL_PROPS:
                exec('tabpanel.'+var +' = p.' + var)
    return draw_tabs_list
        
                            
def drawRegionUI(self,context):#, getspace, getregion, tabID):
    #print(dir(self))
   
    tabID = self.bl_idname
    
    draw_tabs_list = getFilteredTabs(self,context)
   # print('pre',self.tabcount)
    
    draw_panels = drawTabs(self, context, draw_tabs_list, tabID)       
    drawPanels(self, context, draw_panels)
    

class ActivatePanel(bpy.types.Operator):
    """activate panel"""
    bl_idname = 'wm.activate_panel'
    bl_label = 'activate panel'
    bl_options = {'REGISTER'}
    
    tabpanel_id = bpy.props.StringProperty(name="tab panel name",
                default='PROPERTIES_PT_tabs')
    panel_id = bpy.props.StringProperty(name="panel name",
                default='')
    
    
    def execute(self, context):
        #unhide_panel(self.tabpanel_id)
        tabpanel = eval('bpy.types.' + self.tabpanel_id )
        s =bpy.context.scene
        s.panelTabData[self.tabpanel_id].active_tab = self.panel_id
        panel = tabpanel
        if bpy.context.scene.panelData.get(self.panel_id) == None:
            item = bpy.context.scene.panelData.add()
            item.name = self.panel_id
        return {'FINISHED'}

        
        
class PopupPanel(bpy.types.Operator):
    """activate panel"""
    bl_idname = 'wm.popup_panel'
    bl_label = 'popup_panel'
    bl_options = {'REGISTER'}
    
    
    tabpanel_id = bpy.props.StringProperty(name="tab panel name",
                default='PROPERTIES_PT_tabs')
    panel_id = bpy.props.StringProperty(name="panel name",
                default='')
    
     
    def draw_panel(self, layout, pt):
        try:
            if hasattr(pt, "poll") and not pt.poll(bpy.context):
                print("POLL")
                return
        except:
            print("POLL")
            return
        
        p = pt(bpy.context.window_manager)
        p.layout = layout.box()
        p.draw(bpy.context)
        '''
        try:
            if hasattr(p, "draw"):
                if isinstance(p.draw, types.MethodType):
                     p.draw(bpy.context)
                else:
                    p.draw(p, bpy.context)
        except:
            pass
        '''
 
    def draw(self, context):
        layout = self.layout
        tp = _hidden_panels[self.panel_id]
       # tp = eval('bpy.types.' + self.panel_id )
        self.draw_panel(layout, tp)
 
    def execute(self, context):
        return {'FINISHED'}
 
    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self)
        
class ActivateModifier(bpy.types.Operator):
    """activate modifier"""
    bl_idname = 'object.activate_modifier'
    bl_label = 'activate modifier'
    bl_options = {'REGISTER'}
    
    modifier_name = bpy.props.StringProperty(name="Modifier name",
                default='')
    
    
    def execute(self, context):
        ob = bpy.context.active_object
        ob.active_modifier = self.modifier_name
        return {'FINISHED'}
    
class ActivateConstraint(bpy.types.Operator):
    """activate constraint"""
    bl_idname = 'object.activate_constraint'
    bl_label = 'activate constraint'
    bl_options = {'REGISTER'}
    
    constraint_name = bpy.props.StringProperty(name="Constraint name", default='')
    
    
    def execute(self, context):
        ob = bpy.context.active_object
        ob.active_constraint = self.constraint_name
        return {'FINISHED'}  
        
class ActivatePoseBoneConstraint(bpy.types.Operator):
    """activate constraint"""
    bl_idname = 'object.activate_posebone_constraint'
    bl_label = 'activate constraint'
    bl_options = {'REGISTER'}
    
    constraint_name = bpy.props.StringProperty(name="Constraint name",
                default='')
    
    
    def execute(self, context):
        pb = bpy.context.pose_bone
        pb.active_constraint = self.constraint_name
        return {'FINISHED'}  
        
class TabsPanel:
    @classmethod
    def poll(cls, context):
        
        tabspanel_info = bpy.types.Scene.panelTabInfo.get(cls.bl_idname)
        if tabspanel_info == None:
            return True
        possible_tabs = tabspanel_info[1]
        draw_tabs_list = pollTabs(possible_tabs, context)
        #print(cls.bl_region_type,cls.bl_space_type,len(draw_tabs_list),len(tabspanel_info[1]))
        #if tabspanel_info!= None:
           # c = len(pollTabs(tabspanel_info[1], context))
            #print('poll',cls.bl_idname, c, len(tabspanel_info[1]))
        return tabspanel_info==None or len(draw_tabs_list) >1
 
 
   
#THIS FUNCTION DEFINES ALL THE TABS PANELS.!!! 
def createPanels():
    spaces = bpy.types.Scene.panelSpaces
    definitions=[]
    panelIDs = []
    pdef = "class %s(TabsPanel,bpy.types.Panel):\n    bl_space_type = '%s'\n    bl_region_type = '%s'\n    %s\n    COMPAT_ENGINES = {'BLENDER_RENDER', }\n    bl_label = ''\n    bl_options = {'HIDE_HEADER'}\n    bl_idname = '%s'\n    draw = drawRegionUI\n"
    for sname in spaces:
        space = spaces[sname]
        for rname in space:
            region = space[rname]
            
            
            categories={}
            contexts={}
            for panel in region:
                if hasattr(panel, 'bl_category'):
                    categories[panel.bl_category] = 1
                if hasattr(panel, 'bl_context'):
                    contexts[panel.bl_context] = 1
            if len(categories)>0:
                for cname in categories:
                    cnamefixed = cname.upper();
                    cnamefixed = cnamefixed.replace(' ','_')
                    cnamefixed = cnamefixed.replace('/','_')
                    pname = '%s_PT_%s_%s_tabs' %(sname.upper(), rname.upper(), cnamefixed.upper())
                    
                    cstring = pdef % (pname, sname.upper() ,rname.upper(), "bl_category = '%s'" % cname ,pname)
                    
                    definitions.append(cstring)
                    panelIDs.append(pname)
            elif len(contexts)>0:
                for cname in contexts:
                    cnamefixed = cname.upper();
                    cnamefixed = cnamefixed.replace(' ','_')
                    cnamefixed = cnamefixed.replace('/','_')
                    pname = '%s_PT_%s_%s_tabs' %(sname.upper(), rname.upper(), cnamefixed.upper())
                    
                    cstring = pdef % (pname, sname.upper() ,rname.upper(), "bl_context = '%s'" % cname ,pname)
                    
                    definitions.append(cstring)
                    panelIDs.append(pname)
            else:     
                pname = '%s_PT_%s_tabs' %(sname.upper(), rname.upper())
                cstring = pdef % (pname, sname.upper() ,rname.upper(), "",pname)
                definitions.append(cstring)
                panelIDs.append(pname)
                
    return definitions,panelIDs

class VIEW3D_PT_Transform(bpy.types.Panel):
    bl_label = "Transform"
    bl_idname = "VIEW3D_PT_Transform"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    @classmethod
    def poll(cls, context):
        return bpy.context.active_object != None
        
    def draw(self, context):
        layout = self.layout

        ob = context.object
        layout.alignment = 'RIGHT'
        row = layout.row()

        row.column(align = True).prop(ob, "location")
        #align=False);
        row.column(align = True).prop(ob, "lock_location")
        row = layout.row()
        if ob.rotation_mode == 'QUATERNION':
            row.column().prop(ob, "rotation_quaternion", text="Rotation")
            
        elif ob.rotation_mode == 'AXIS_ANGLE':
            #row.column().label(text="Rotation")
            #row.column().prop(pchan, "rotation_angle", text="Angle")
            #row.column().prop(pchan, "rotation_axis", text="Axis")
            row.column().prop(ob, "rotation_axis_angle", text="Rotation")
            
        else:
            row.column().prop(ob, "rotation_euler", text="Rotation")
        row.column(align = True).prop(ob, "lock_rotation")
        layout.prop(ob, "rotation_mode", text='')
        row = layout.row()
        row.column().prop(ob, "scale")
        row.column(align = True).prop(ob, "lock_scale")


def modifiersDraw(self, context):
    variable_width = bpy.context.user_preferences.addons["tabs_interface"].preferences.variable_width

    wtabcount = getWTabCount(context)
        
    layout = self.layout

    ob = context.object
    layout.operator_menu_enum("object.modifier_add", "type")
    
    
    if len(ob.modifiers)>0:
        i=0
        col = layout.column(align = True)
        row = tabRow(col)
        active_modifier = ob.active_modifier
        if not ob.active_modifier in ob.modifiers:
            active_modifier = ob.modifiers[0].name
        if len(ob.modifiers)>1:
            for md in ob.modifiers:
                
                if md.name==active_modifier:
                    op = row.operator("object.activate_modifier", text=md.name, emboss = False).modifier_name = md.name
                else:
                    op = row.operator("object.activate_modifier", text=md.name, emboss = True).modifier_name = md.name
                i+=1
                if i == wtabcount:
                    i=0
                    row = tabRow(col)
        
        
        md = ob.modifiers[active_modifier]
        box = layout.template_modifier(md)
        if box:
            # match enum type to our functions, avoids a lookup table.
            getattr(self, md.type)(box, ob, md)

def constraintsDraw(self, context):
    wtabcount = getWTabCount(context)
    

    layout = self.layout

    ob = context.object

    if ob.type == 'ARMATURE' and ob.mode == 'POSE':
        box = layout.box()
        box.alert = True  # XXX: this should apply to the box background
        box.label(icon='INFO', text="Constraints for active bone do not live here")
        box.operator("wm.properties_context_change", icon='CONSTRAINT_BONE',
                     text="Go to Bone Constraints tab...").context = 'BONE_CONSTRAINT'
    else:
        layout.operator_menu_enum("object.constraint_add", "type", text="Add Object Constraint")
    
    if len(ob.constraints)>0:
        col = layout.column(align = True)
        row = tabRow(col)
        i=0
        active_constraint = ob.active_constraint
        if not ob.active_constraint in ob.constraints:
            active_constraint = ob.constraints[0].name
        if len(ob.constraints)>1:
            for con in ob.constraints:
                if con.name==active_constraint:
                    op = row.operator("object.activate_constraint", text=con.name, emboss = False)
                else:
                    op = row.operator("object.activate_constraint", text=con.name, emboss = True)
                op.constraint_name = con.name
                i+=1
                if i == wtabcount:
                    i=0
                    row = tabRow(col)
        
        con = ob.constraints[active_constraint]
        self.draw_constraint(context, con)    
       
      
def boneConstraintsDraw(self, context):
    wtabcount = getWTabCount(context)
    layout = self.layout

    layout.operator_menu_enum("pose.constraint_add", "type", text="Add Bone Constraint")
    pb = context.pose_bone
    
    
    if len(pb.constraints)>0:
    
        col = layout.column(align = True)
        row = col.row(align = True)
        i=0
        active_constraint = pb.active_constraint
        if not pb.active_constraint in pb.constraints:
            active_constraint = pb.constraints[0].name
        if len(pb.constraints)>1:
            for con in pb.constraints:
                if con.name==active_constraint:
                    op = row.operator("object.activate_posebone_constraint", text=con.name, emboss = False)
                else:
                    op = row.operator("object.activate_posebone_constraint", text=con.name, emboss = True)
                op.constraint_name = con.name
                i+=1
                if i == wtabcount:
                    i=0
                    row = col.row(align = True)
        
        con = pb.constraints[active_constraint]
        self.draw_constraint(context, con)    
    
class TabInterfacePreferences(bpy.types.AddonPreferences):
    bl_idname = "tabs_interface"
    # here you define the addons customizable props
    variable_width = bpy.props.BoolProperty(name = 'Tabs width by name length', default=True)

    # here you specify how they are drawn
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "variable_width")
    
    
 

def createSceneTabData():
    s = bpy.context.scene
    #print('handler')
    for pname in bpy.types.Scene.panelIDs:
        p = bpy.types.Scene.panelIDs[pname]
        if s.panelData.get(p.realID) == None:
            item = bpy.context.scene.panelData.add()
            item.name = p.realID  
    #print(_tab_panels)
    for pt in _tab_panels:
        print(pt)
        if s.panelTabData.get(pt) == None:
            item = bpy.context.scene.panelTabData.add()
            item.name = pt
    
@persistent
def scene_load_handler(scene):
    if len(bpy.context.scene.panelData) == 0:
        createSceneTabData()
    
    
@persistent
def object_select_handler(scene):
    s = bpy.context.scene
    #print('handler')
    if bpy.context.active_object:
        if not hasattr(s,'active_previous'):
            #print('firsttime')
            s.active_previous = bpy.context.active_object.name
        if bpy.context.active_object.name != s.active_previous:
            #print("Selected object", bpy.context.active_object.name)
            s.active_previous = bpy.context.active_object.name
        

def register():
    
    bpy.utils.register_class(VIEW3D_PT_Transform)#we need this panel :()

    bpy.types.Scene.panelIDs = getPanelIDs()
    #if not hasattr(bpy.types.Scene, 'panels'):# or random.random()<0.01:
     #   bpy.types.Scene.panels = getPanelIDs()
        #if not hasattr(bpy.types.Scene, 'panelSpaces'):
      #  bpy.types.Scene.panelSpaces = buildTabDir()
    bpy.types.Scene.panelSpaces = buildTabDir()
    bpy.types.Scene.panelTabInfo = {}
    #build the classess here!!
    definitions, panelIDs = createPanels()
    for d in definitions:
        #print(d)
        exec(d)
    for pname in panelIDs:
        #print('register ', pname)
        p = eval(pname)
        bpy.utils.register_class(eval(pname))
        pt = eval('bpy.types.'+pname)
        _tab_panels[pname] = pt
    bpy.utils.register_class(ActivatePanel)
    bpy.utils.register_class(PopupPanel)
    bpy.utils.register_class(ActivateModifier)
    bpy.utils.register_class(ActivateConstraint)
    bpy.utils.register_class(ActivatePoseBoneConstraint)
    bpy.utils.register_class(tabSetups)
    bpy.utils.register_class(panelData)
    bpy.utils.register_class(TabInterfacePreferences)
    
    bpy.types.DATA_PT_modifiers.draw = modifiersDraw
    bpy.types.OBJECT_PT_constraints.draw = constraintsDraw
    bpy.types.BONE_PT_constraints.draw = boneConstraintsDraw
    
    bpy.types.Scene.active_previous = bpy.props.StringProperty(name = 'active object previous', default = '')
    bpy.types.Object.active_modifier = bpy.props.StringProperty(name = 'active modifier', default = '')
    bpy.types.Object.active_constraint = bpy.props.StringProperty(name = 'active constraint', default = '')
    bpy.types.PoseBone.active_constraint = bpy.props.StringProperty(name = 'active constraint', default = '')
    bpy.types.Scene.panelTabData = bpy.props.CollectionProperty(type=tabSetups)
    bpy.types.Scene.panelData = bpy.props.CollectionProperty(type=panelData)
    bpy.app.handlers.load_post.append(scene_load_handler)
    #bpy.app.handlers.scene_update_pre.append(scene_load_handler)
    
        
   
    
     
    
def unregister():
    #first, fix the panels:
    for panel in bpy.types.Scene.panelIDs:
        
        if hasattr(panel, 'bl_category'):
            if hasattr(panel, 'orig_category'):
                panel.bl_category = panel.orig_category
        unhide_panel(panel.realID)
        
    bpy.utils.unregister_class(VIEW3D_PT_Transform)
    
    
    
    definitions, panelIDs = createPanels()
    for d in definitions:
        #print(d)
        exec(d)
    for pname in panelIDs:
        #print('unregister ', pname)
        if hasattr(bpy.types, pname):
            bpy.utils.unregister_class(eval('bpy.types.'+pname))
    
    bpy.utils.unregister_class(ActivatePanel)
    bpy.utils.unregister_class(PopupPanel)
    bpy.utils.unregister_class(ActivateModifier)
    bpy.utils.unregister_class(ActivateConstraint)
    bpy.utils.unregister_class(ActivatePoseBoneConstraint)
    bpy.utils.unregister_class(tabSetups)
    bpy.utils.unregister_class(panelData)
    bpy.utils.unregister_class(TabInterfacePreferences)
    

if __name__ == "__main__":
    register()
    
    #https://github.com/meta-androcto/blenderpython/tree/master/scripts/addons_extern/AF_view3d_mod https://github.com/meta-androcto/blenderpython/tree/master/scripts/addons_extern/AF_view3d_toolbar_mod