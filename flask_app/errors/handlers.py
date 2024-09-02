from flask import Blueprint, render_template

errors = Blueprint("errors", __name__)

#decorators
#there is another method called errorhandler() which will be applicable for only this particular blueprint
#so we need to use the app_errorhandler() to make it available or applicable accross the entire application

#############################################################################################
####################################  404 Error #############################################
#############################################################################################

@errors.app_errorhandler(404)
def error_404(error):
    return render_template("errors/404.html"), 404 #second value is the status code and the default is 200(success)

#############################################################################################
####################################  403 Error #############################################
#############################################################################################

@errors.app_errorhandler(403)
def error_403(error):
    return render_template("errors/403.html"), 403 #second value is the status code and the default is 200(success)

#############################################################################################
####################################  500 Error #############################################
#############################################################################################

@errors.app_errorhandler(500)
def error_500(error):
    return render_template("errors/500.html"), 500 #second value is the status code and the default is 200(success)