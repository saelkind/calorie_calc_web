from flask.views import MethodView
from flask import Flask, render_template, url_for, send_from_directory, request

# using  wtforms library for HTML form framework
from wtforms import Form, StringField, DateField, IntegerField, \
    SubmitField, DecimalField, RadioField
from wtforms.validators import NumberRange, Length, DataRequired, InputRequired

# model classes
from model.height import Height
from model.person import Person
from model.location import Location

app = Flask(__name__)


class UnitsForm(Form):
    units_selection = RadioField("Units of measurement", choices=[("Metric", 'Metric'), ("English",'English')],
                             validators=[InputRequired()], coerce=str)
    button = SubmitField("Go to calculation")

class HomePage(MethodView):
    def get(self):
        # flask knows all templates are in the templates sub dir
        units_form = UnitsForm()
        return render_template("index.html", unitsform=units_form)



class CaloriesForm(Form):
    height_centimeters = DecimalField("Height (cm)",
                                validators=[NumberRange(15.0, 249.9, InputRequired())])
    height_feet = IntegerField("Height (ft)", description="Whole numbers only please",
                                validators=[NumberRange(1, 7), InputRequired()])
    height_inches = DecimalField("Height (in)",
                                validators=[NumberRange(0.0, 11.99999), InputRequired()])
    age = IntegerField("Age",
                                validators=[NumberRange(1, 125), InputRequired()])
    weight_kg = DecimalField("Weight (kg)",
                                validators = [NumberRange(10.0, 199.9), InputRequired()])
    weight_pounds = DecimalField("Weight(lb)",
                                validators = [NumberRange(50.0, 399.9), InputRequired()])
    city = StringField("City",
                                validators=[Length(3, 50), InputRequired()])
    country = StringField("Country",
                                validators=[Length(2, 50), InputRequired()])
    button = SubmitField("Calculate Calories")

class CaloriesFormPage(MethodView):
    def get(self):
        # app.logger.debug(request.form)
        # app.logger.debug(request.data)
        #  OK, I figured it out.  In the GET method, you need to use
        #  request.args, no request.form, to create the Form object
        units_form = UnitsForm(request.args)
        # app.logger.debug(units_form.data)
        is_metric = units_form.data["units_selection"] == "Metric"
        cal_form = CaloriesForm()
        return render_template('calories.html',
                               calform=cal_form,
                               ismetric=is_metric)

    def post(self):
        # app.logger.debug(request.form)
        cal_form = CaloriesForm(request.form)
        # app.logger.debug(cal_form.data)
        is_metric = cal_form.weight_kg.data is not None
        # app.logger.debug(cal_form.weight_kg)
        # app.logger.debug(f"1. cal_form.weight_kg.data {cal_form.weight_kg.data}")
        # app.logger.debug(f"1. cal_form.weight_pounds.data {cal_form.weight_pounds.data}")
        # app.logger.debug(f"2. is_metric {is_metric}")
        person = None
        height = Height()
        if is_metric:
            person = Person(cal_form.age.data, float(cal_form.weight_kg.data), True)
            person.height = height
            height.set_metric(float(cal_form.height_centimeters.data))
        else:
            person = Person(cal_form.age.data, float(cal_form.weight_pounds.data), False)
            person.height = height
            height.set_english(int(cal_form.height_feet.data), float(cal_form.height_inches.data))

        person.location = Location(cal_form.city.data, cal_form.country.data)
        try:
            calories_needed = person.calc_calories_needed()
            if is_metric:
                temperature_str = person.location.temp_data[Location.METRIC_STR_KEY]
            else:
                temperature_str = person.location.temp_data[Location.ENGLISH_STR_KEY]
            results_str = f"With the current temperature of {temperature_str}, you will need \
                       to consume {calories_needed} calories today."
        except ValueError as ve:
            results_str = f"{ve}"

        return render_template('calories.html',
                               calform=cal_form,
                               ismetric=is_metric,
                               results=True,
                               resultsstr=results_str)


app.add_url_rule('/', view_func=HomePage.as_view('home_page'))
app.add_url_rule('/calories', view_func=CaloriesFormPage.as_view('calories'), methods=["GET", "POST"])

app.run(debug=True)
