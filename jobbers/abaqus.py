import os
import glob
import inquirer  # https://pypi.org/project/inquirer/
import jinja2    # http://jinja.pocoo.org/docs/2.10/
import jobbers.jobber
from pprint import pprint
#
# Abaqus jobber.
#

def list_inputfiles(path=None):
    """ Returns a list of inputfiles in a directory ( default: pwd) """
    if not path:
        path = os.getcwd()

    files = glob.glob(os.path.join(path, '*.inp'))
    print(files)
    return(glob.glob(os.path.join(path, '*.inp')))

    
def process():
    """ Returns a rendered template, 
    based on questions from inquirer
    as a string to stdout """

    # Templates relative to the package
    templates_dir=os.path.join(os.path.dirname(jobbers.jobber.__file__), 'templates')

    questions = [

        inquirer.List('jobclass',
                       message="Select Abaqus Analysistype",
                       choices=[
                           ('Standard','abaqus-standard.tmpl.j2'),
                           ('Eigenfrequency','abaqus-eigenfrequency.tmpl.j2'),
                           ('Syntaxcheck','abaqus-syntaxcheck.tmpl.j2'),
                           ('Python','abaqus-python.tmpl.j2'),
                           ('Datacheck', 'abaqus-datacheck.tmpl.j2'),
                           ('Explicit (single or double precision)','abaqus-explicit.tmpl.j2'),
                           ('Trivial)','abaqus-core.tmpl.j2'),
                       ],),

        inquirer.Path('inputfile',
                      message="Input file (absolute path)",
                      path_type=inquirer.Path.FILE,
                      exists=True,
                      default=next(iter(list_inputfiles()), None )),

        inquirer.List('abaqusversion',
                      message="Abaqus module version (Includes environment-module in job)",
                      choices=['6.12-3',
                               '6.13-2',
                               '6.14-2',
                               '2016',
                               '2017.1 (2017.HF8)',
                               '2018-2 (2018.HF5)'] ),
        inquirer.List('account',
                      message="Which Account to run under? (SLURM)",
                      choices=[('Techsim','techsim'),
                               ('IUBA', 'iuba'),
                               ('Commonwealth', 'default'),
                               ('None', '')], ),
    ]

    answers = inquirer.prompt(questions)

    # pprint(answers)        

    templatequestion = inquirer.Path('template',
                             message="Which template shall be used?",
                             path_type=inquirer.Path.FILE,
                             exists=True,
                             default=("{}/{}").format( templates_dir, answers['jobclass'] ) ),
        
    tmpl_answers = inquirer.prompt(templatequestion)

    pprint(tmpl_answers)
    
    TEMPLATE_FILE = tmpl_answers['template']
    
    with open(TEMPLATE_FILE) as file_:
        template = jinja2.Template(file_.read())
    
    outputText = template.render(answers=answers, template=tmpl_answers)  # this is where to put args to the template renderer

    return outputText
