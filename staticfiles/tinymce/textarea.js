HACKED existence
blog
hackerfridge
projects
members
contact
Django Tutorial - Video 4 - TinyMCE
This tutorial walks through installing the django-tinymce package to provide a WYSIWYG editor for TextField's in the django admin interface.



The django-tinymce project's github page can be found here:

https://github.com/aljosa/django-tinymce

copy the 'tinymce' folder to the django project root

add 'tinymce' to INSTALLED_APPS in settings.py

$ python manage.py syncdb
If you get the following error:

ImportError: cannot import name smart_unicode
in tinymce/widgets.py change

from django.forms.util import smart_unicode
to

from django.utils.encoding import smart_unicode
add (r'^tinymce/', include('tinymce.urls')) to urls.py

cp -r tinymce/media/tiny_mce/ /path/to/your/static/js/

in admin.py for the app you want to add TinyMCE to, create the TinyMCEAdmin class

class TinyMCEAdmin(admin.ModelAdmin):
        class Media:
                js = ('/media/js/tiny_mce/tiny_mce.js', '/media/js/tiny_mce/textareas.js',)
textareas.js:

tinyMCE.init({
    // General options
    mode : "textareas",
    theme : "advanced",
    plugins : "pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template,wordcount,advlist,autosave",

// Theme options
theme_advanced_buttons1 : "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,fontselect,fontsizeselect,fullscreen,code",
theme_advanced_buttons2 : "bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,|,forecolor,backcolor",
theme_advanced_buttons3 : "tablecontrols,|,hr,sub,sup,|,charmap",

theme_advanced_toolbar_location : "top",
theme_advanced_toolbar_align : "left",
theme_advanced_statusbar_location : "bottom",
theme_advanced_resizing : true,

// Example content CSS (should be your site CSS)
//content_css : "/css/style.css",

template_external_list_url : "lists/template_list.js",
external_link_list_url : "lists/link_list.js",
external_image_list_url : "lists/image_list.js",
media_external_list_url : "lists/media_list.js",

// Style formats
style_formats : [
    {title : 'Bold text', inline : 'strong'},
    {title : 'Red text', inline S: 'span', styles : {color : '#ff0000'}},
    {title : 'Help', inline : 'strong', classes : 'help'},
    {title : 'Table styles'},
    {title : 'Table row 1', selector : 'tr', classes : 'tablerow'}
],

width: '700',
height: '400'
});
©2009-2012 HackedExistence. All Rights Reserved. Site by C2G