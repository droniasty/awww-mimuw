import json
import os
import subprocess
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
#from django.template import loader
#import requests
from awwwapp.models import FileSection, SectionStatus, User, Catalog, File, SectionKind
import pdb
import re
from  awwwapp.globals import *

#from django import forms

#from awwwlab.awwwapp.forms import StandardForm

def login_viev(request):
    #default_user()
    # get user with the smallest id
    #user = User.objects.all().order_by('id')[0]
    #request.session['user_id'] = user.id
    #request.session['selected_catalog_id'] = 0
    #request.session['file_id'] = 0
    #return redirect('/frontend')
    return render(request, 'login.html')

def register_viev(request):
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']
        #user = authenticate(request, login=login, password=password)
        user = User.objects.filter(login=login, password=password)
        if user:
            #login(request, user)
            request.session['user_id'] = user[0].id
            request.session['selected_catalog_id'] = 0
            request.session['file_id'] = 0
            #return render(request, 'frontend.html')
            return redirect('/frontend')
        else:
            return render(request, 'error.html')
    #return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        login = request.POST['login']
        password = request.POST['password']
        # create user object in database
        newUser = User.objects.create(
            name=name,
            login=login,
            password=password,
        )
        newUser.save()
    return render(request, 'login.html')

def frontend(request):
    #user_id = request.session['user_id']
    #print("user_id: ", user_id)
    default_section_kinds()
    default_section_status()

    # change value of full_content_json which is declared in globals.py to user_catalogs(user_id) to get catalog tree
    #full_content_json = user_catalogs(user_id)
    #f = open('awwwapp/templates/UserContent.json', 'w')
    #f.write(full_content_json)
    #f.close()
    return render(request, 'frontend.html')

def user_catalogs(request):
    if not request.session.has_key('user_id'):
        # find user with name test and set session['user_id'] to his id
        user = User.objects.get(name='test')   
        request.session['user_id'] = user.id 
        request.session['selected_catalog_id'] = 0
    user_id = request.session['user_id']
    #print("user_id: ", user_id)
    user = get_object_or_404(User, id=user_id)
    catalog_list = Catalog.objects.filter(owner=user).filter(supercatalog=None).filter(accessibility_marker=True)
    full_content = []
    #print("starting for")
    for catalog in catalog_list:
        #files = File.objects.filter(catalog=catalog).filter(accessibility_marker=True)
        full_content.append({'id': catalog.id, 'name': catalog.name, 'type': 'catalog', 'depth': ''})
        #files = [{'id': file.id, 'name': file.name, 'type': 'file', 'depth': ''} for file in files]
        #full_content.extend(files)
        catalog_id = catalog.id
        cc = catalog_contents(catalog_id,' ')
        full_content.extend(cc)
    # return render(request, 'catalogs.html', {'full_content': full_content})
    #full_content = json.dumps(full_content)
    # open file templates/UserContent.json and remove all content
    #print("returning full_content")
    return JsonResponse(full_content, safe=False)

'''
def cataloges_view(request):
    catalogs = Catalog.objects.all()
    return render(request, 'frontend.html', {'catalogs': catalogs})


def program_view(request, file_id):
    file = get_object_or_404(File, id=file_id)
    sections = FileSection.objects.filter(file=file)
    sections = sorted(sections, key=lambda section: section.start)
    program_text = ""
    for section in sections:
        program_text += section.content + "\n"
    return render(request, 'program.html', {'program_text': program_text})
'''


def program_code_view(request):
    file_id = request.session['file_id']
    text = collect_file_content(file_id)
    #print(text) # here the text sill has newlines
    #text_with_breaks = text.replace('&','&amp;').replace('"','&quot;').replace(' ', '&nbsp;').replace('<', '&lt;').replace('>', '&gt;')#.replace('\n', '<br>')
    #text_with_breaks = text_with_breaks.split('\n')
    #html_list = []
    #i = 0
    #for line in text_with_breaks:
    #    html_list.append('<div class="codeline" id="prog_line_' + str(i) + '">' + line + '</div>')
    #    i += 1
    #text_with_breaks = ''.join(html_list)
    
    return HttpResponse(text)

'''
def change_standard_view(request):
    if request.method == 'POST':
        standard = request.POST.get('standard')
        change_standard(standard)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def change_processor_view(request):
    if request.method == 'POST':
        processor = request.POST.get('processor')
        change_processor(processor)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def change_optimization_view(request):
    # optimizations = compiler_options['optimizations']
    if request.method == 'POST':
        optimization = request.POST.get('optimization')
        chnge_optimizations(optimization)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def change_specyfic_view(request):
    # specyfic = compiler_options['specyfic']
    if request.method == 'POST':
        specyfic = request.POST.get('specyfic')
        change_specyfic(specyfic)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
'''

def add_file_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        file = request.FILES.get('file')

        # Access the form data
        print('Name:', name)
        print('Description:', description)
        print('File:', file)
        catalog_id = request.session['selected_catalog_id']
        print("catalog_id: ", catalog_id)
        user_id = request.session['user_id']
        owner = get_object_or_404(User, id=user_id)
        
        # create the File object
        new_file = File.objects.create(
            name=name,
            description=description,
            owner=owner,
            catalog_id=catalog_id,
            accessibility_marker=True
        )
        # save the object to the database
        new_file.save()

        # get the file content
        file_content = file.read()
        # get file content in a form of list of lines
        file_content = file_content.decode('utf-8').splitlines()
        # find the number otf the last line which starts with '#'
        last_directive_line = 0
        for line in file_content:
            if line.startswith('#'):
                last_directive_line += 1
            else:
                break

        directives_content = file_content[:last_directive_line]
        # merge it into single string
        directives_content = '\n'.join(directives_content)
        # create the FileSection objects

        # create the FileSection object for the file header
        directives_status = SectionStatus.objects.create(
            name='Not tried',
        )
        directives_status.save()
        directives_file_section = FileSection.objects.create(
            file=new_file,
            kind=SectionKind.objects.get(name='compiler directive'),
            start=0,
            end=last_directive_line,
            status=directives_status,
            content=directives_content
        )
        directives_file_section.save()

        # check if there is a line starting with 'typedef'
        typedef = False
        last_typedef_line = 0
        for line in file_content:
            if line.startswith('typedef'):
                typedef = True
                break
        
        if typedef:
            # find the number of the last line which starts with 'typedef'
            for line in file_content:
                if line.startswith('typedef'):
                    last_typedef_line += 1
                else:
                    break
            
            # create the FileSection object for the typedefs
            typedefs_content = file_content[last_directive_line:last_typedef_line]
            typedefs_content = '\n'.join(typedefs_content)
            typedefs_status = SectionStatus.objects.create(
                name='Not tried',
            )
            typedefs_status.save()
            typedefs_file_section = FileSection.objects.create(
                file=new_file,
                kind=SectionKind.objects.get(name='variable declaration'),
                start=last_directive_line,
                end=last_typedef_line,
                status=typedefs_status,
                content=typedefs_content
            )
            typedefs_file_section.save()

        # create the FileSection object for the file body
        body_content = file_content[max(last_directive_line,last_typedef_line):]
        body_content = '\n'.join(body_content)
        body_status = SectionStatus.objects.create(
            name='Not tried',
        )
        body_status.save()
        body_file_section = FileSection.objects.create(
            file=new_file,
            kind=SectionKind.objects.get(name='code'),
            start=max(last_directive_line,last_typedef_line),
            end=len(file_content),  
            status=body_status,
            content=body_content
        )
        body_file_section.save()
        #reset_globals()
        return HttpResponse('')
        #return redirect('/frontend')

        # add the file content to the object
        # new_file.file_content.save(name, file)

        #return HttpResponse('File uploaded successfully.')

    return HttpResponse('File upload failed.')

def create_catalog_viev(request):
    #return render(request, 'error.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        #print(name)
        description = request.POST.get('description')
        #check if user is logged in
        if not request.session.has_key('user_id'):
            # find user with name test and set session['user_id'] to his id
            user = User.objects.get(name='test')   
            request.session['user_id'] = user.id 
            request.session['selected_catalog_id'] = 0
        user_id = request.session['user_id']
        parent_catalog_id = request.session['selected_catalog_id']
        #print(user_id)
        owner = User.objects.get(id=user_id)
        #print("gotowner")
        #parent_catalog_id = selected_catalog_id
        supercatalog = None
        print(parent_catalog_id)
        if parent_catalog_id:
            supercatalog = Catalog.objects.get(id=parent_catalog_id)
        #print(parent_catalog_id)
        new_catalog = Catalog.objects.create(
            name=name,
            description=description,
            owner=owner,
            supercatalog=supercatalog,
            accessibility_marker=True
        )
        new_catalog.save()
        #reset_globals()
        #return redirect('/frontend')
        return JsonResponse({'success': True})
    else:
        return render(request, 'error.html')

    #return redirect('catalog_detail', catalog_id=new_catalog.id)

def get_code(request):
    code = ''
    # get the file with the given id from database
    file_id = request.session['file_id']
    file = get_object_or_404(File, id=file_id)
    # get the file sections
    file_sections = FileSection.objects.filter(file=file)
    # sort the file sections by their start line
    file_sections = sorted(file_sections, key=lambda x: x.start)
    for file_section in file_sections:
        code += file_section.content + '\n'
    # create the file with the code
    with open('code.c', 'w') as f:
        f.write(code)
    # create the command
    sdcc_command = 'sdcc -S '
    if len(compiler_options['processor']) > 0:
        sdcc_command += '-m' + compiler_options['processor'] + ' '
    for optimization in compiler_options['optimization']:
        sdcc_command += optimization + ' '
    for specyfic in compiler_options['specyfic']:
        sdcc_command += specyfic + ' '
    sdcc_command += '--std-' + compiler_options['standard'] + ' '
    #sdcc_command += 'code.c'
    #print(sdcc_command)
    sdcc_cmd = sdcc_command.split() + ['code.c']
    # Run the command and capture the output
    #process = subprocess.Popen(sdcc_command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #stdout, stderr = process.communicate()
    # if there is a file "code.asm" remove it
    if os.path.exists('code.asm'):
        os.remove('code.asm')
    try:
        process_output = subprocess.check_output(sdcc_cmd, stderr=subprocess.STDOUT)
        # if there is a file "code.asm" return its content
        if os.path.exists('code.asm'):
            with open('code.asm', 'r') as f:
                asm = f.read()
                #asm = asm.replace('&','&amp;').replace('"','&quot;').replace(' ', '&nbsp;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')
        asm_list = asm.split('\n')
        section_number = 0
        section_header = False
        output_lines = []
        for line in asm_list: # dopisac howanie wszystkich sekcji
            if line.startswith(';-------'):
                if section_header:  # drugie ;----------
                    section_header = False
                else:  # pierwsze ;----------
                    section_header = True
                    section_number += 1 
                output_lines.append('<div class="section_header" onclick="hideShowDivs(\'section' + str(section_number) + '\')" >' + line + '</div>')
            elif section_header: # tekst miedzy ;----------
                output_lines.append('<div class="section_header" onclick="hideShowDivs(\'section' + str(section_number) + '\')" >' + line + '</div>')
            else: # tekst w sekcji
                # check if this line contains code.c substring
                if 'code.c' in line:
                    # get the number just after code.c substring
                    line_number = find_number(line)
                    output_lines.append('<div class="section_content" name="section' + str(section_number) + '" onclick="hightLine(' + str(line_number) + ')">' + line + '</div>')
                else:
                    output_lines.append('<div class="section_content" name="section' + str(section_number) + '">' + line + '</div>')
        return HttpResponse(''.join(output_lines))

        #return HttpResponse(process_output.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        
        return HttpResponse(e.output.decode('utf-8'))

    #return HttpResponse(stdout.decode('utf-8'))
    

    # return HttpResponse(code)

def change_sections_view(request):
    new_sections = request.POST.get('sections').split(' ')
    file = get_object_or_404(File, id=file_id)
    # remove all the sections of this file
    prev_sections = file.file_sections.all()
    code = ''
    for section in prev_sections:
        code += section.content + '\n'
    code = code.splitlines()
    file.file_sections.all().delete()
    starts = [int(x) for x in new_sections]
    starts.sort()
    ends = starts[1:]   
    ends.append(len(code))
    for i in range(len(starts)):
        content = '\n'.join(code[starts[i]:ends[i]])
        new_section = FileSection.objects.create(
            file=file,
            kind=SectionKind.objects.get(name=get_section_kind(content)),
            start=starts[i],
            end=ends[i],
            content=content
        )
        new_section.save()
    # create new sections


####################### HELPERS #############################

def catalog_contents(catalog_id,depth):
    catalog = get_object_or_404(Catalog, id=catalog_id)
    #ret = []
    files = File.objects.filter(catalog=catalog, accessibility_marker=True)
    #print(files)
    ret = [{'id': file.id, 'name': file.name, 'type': 'file', 'depth': depth} for file in files]
    # subcat = su
    for subcatalog in subcatalogs(catalog_id):
        ret.append({'id': subcatalog.id, 'name': subcatalog.name, 'type': 'catalog', 'depth': depth})
        subcatalog_id = subcatalog.id
        subcatalog_contents = catalog_contents(subcatalog_id,depth + ' ')
        ret.extend(subcatalog_contents)

    return ret

def change_processor(request):
    #return render(request, 'error.html')
    processor = request.POST.get('processor')
    #print("processor: " + processor + "\n")
    compiler_options['processor'] = processor
    compiler_options['specyfic'] = []
    #print(compiler_options['processor'])
    return HttpResponse('')

def change_standard(request):
    standard = request.POST.get('standard')
    #print("standard: " + standard + "\n")
    compiler_options['standard'] = standard
    #print(compiler_options['standard'])
    return HttpResponse('')

def change_optimizations(request):
    optimization = request.POST.get('optimization')
    #print("optimization: " + optimization + "\n")
    optimizations = compiler_options['optimization']
    if optimization in optimizations:
        optimizations.remove(optimization)
    else:
        optimizations.append(optimization)
    compiler_options['optimization'] = optimizations
    #print(compiler_options['optimization'])
    return HttpResponse('')
    
def change_specyfic(request):
    specyfic = request.POST.get('specyfic')
    prevspecyfic = compiler_options['specyfic']
    if specyfic in prevspecyfic:
        prevspecyfic.remove(specyfic)
    else:
        prevspecyfic.append(specyfic)
    compiler_options['specyfic'] = prevspecyfic
    print(compiler_options['specyfic'])
    return HttpResponse('')

'''
def change_compiler_options(which, value):
    print("which: " + which + " value: " + value + "\n")
    global compiler_options
    compiler_options[which] = value
'''

def delete_file(request):
    # set accessibility_marker of file with id = file_id to False if file id is not 0 and file owner is the same as user
    file_id = request.session.get('file_id')
    if file_id != 0:
        file = get_object_or_404(File, id=file_id)
        #if file.owner == requests.user:
        file.accessibility_marker = False
        file.save()
    #file_id = 0
    request.session['file_id'] = 0
    return HttpResponse('')

def delete_catalog(request):
    # set accessibility_marker of catalog with id = catalog_id to False if catalog id is not 0 and catalog owner is the same as user
    selected_catalog_id = request.session.get('selected_catalog_id')
    if selected_catalog_id != 0:
        catalog = get_object_or_404(Catalog, id=selected_catalog_id)
        #if catalog.owner == requests.user:
        catalog.accessibility_marker = False
        catalog.save()
    #selected_catalog_id = 0
    request.session['selected_catalog_id'] = 0
    #return redirect('/frontend')
    return HttpResponse('')

def collect_file_content(file_id):
    # collect content of file with id = file_id
    file = get_object_or_404(File, id=file_id)
    file_sections = FileSection.objects.filter(file=file)
    # sort sections by start
    file_sections = sorted(file_sections, key=lambda section: section.start)
    program_text = ""
    for section in file_sections:
        program_text += section.content + "\n"
    return program_text

def change_selected_catalog_id(request):
    request.session['selected_catalog_id'] = request.POST.get('catalog_id')
    print(request.session['selected_catalog_id'])
    #print("selected_catalog_id: " + selected_catalog_id + "\n")
    #catalog_id = request.POST.get('catalog_id')
    #selected_catalog_id = catalog_id
    #print("selected_catalog_id: " + selected_catalog_id + "\n")
    return HttpResponse('')

def get_selected(request):
    session_data = {
        'file_id': request.session.get('file_id'),
        'selected_catalog_id': request.session.get('selected_catalog_id'),
        # Add other session variables you need
    }
    print(session_data)
    return JsonResponse(session_data)

def change_file_id(request):
    request.session['file_id'] = request.POST.get('file_id')
    #print("file_id: " + file_id + "\n")
    #id = request.POST.get('file_id')
    #file_id = id
    #print("file_id: " + file_id + "\n")
    return HttpResponse('')

def get_section_kind(content):
    if content[0] == '#':
        return  'compiler directive'
    elif content[0] == '/':
        return 'comment'
    # if contect starts with 'void'
    elif content[0:4] == 'void':
        return 'procedure'
    # if content starts with 'typedef'
    elif content[0:7] == 'typedef':
        return 'variable declaration'
    # if content starts with 'asm'
    elif content[0:3] == 'asm':
        return 'assembly'
    else :
        return 'code'
    
def subcatalogs(catalog_id):
    subcatalogs = Catalog.objects.filter(supercatalog_id=catalog_id).filter(accessibility_marker=True)
    return subcatalogs 

def default_section_kinds():
    kinds = ['procedure', 'comment', 'code', 'compiler directive','variable declaration', 'assembly code']
    for kind in kinds:
        # check if kind exists
        if not SectionKind.objects.filter(name=kind).exists():
            new_kind = SectionKind.objects.create(name=kind)
            new_kind.save()

def default_section_status():
    status = ['compiled', 'not compiled', 'compiled with warnings']
    for stat in status:
        # check if status exists
        if not SectionStatus.objects.filter(name=stat).exists():
            new_stat = SectionStatus.objects.create(name=stat)
            new_stat.save()


def find_number(text):
    pattern = r'\d+'  # Matches one or more digits
    match = re.search(pattern, text)
    return int(match.group()) if match else None
    '''
    if match:
        return int(match.group())
    else:
        return None
    '''

'''
def default_user():
    # if user table is empty, create admin
    if not User.objects.all().exists():
        admin = User.objects.create(
            name='admin',
            login='admin',
            password='admin',
        )
        admin.save()

'''

    
# Create your views here.
