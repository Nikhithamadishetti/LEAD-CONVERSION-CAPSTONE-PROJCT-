# -*- coding: utf-8 -*-
"""
Created on Sat May 23 13:29:29 2020

@author: Delll
"""


from flask import Flask, render_template
import pickle
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, validators, StringField, IntegerField, FloatField, SelectField
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from PIL import Image
from io import BytesIO
from base64 import b64encode
import pandas as pd
#pd.set_option('display.max_colwidth', -1)

# code which helps initialize our server
app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret key'

bootstrap = Bootstrap(app)
converted_index=['1','0'] 

# load the model from disk
model = pickle.load(open('model/model.pkl', 'rb'))

program_type_index=['Certificate','Undergraduate','Graduate','None']
programsubtype_index=['Pyschology','Business','Project Management','Human Resourse & Leadership','Six Sigma','Other values']
uian_index=['Villanova University','Florida Institute of Technology','Michigan State University','New England College','University of Notre Dame','Other values']
inquiry_source_index=['cpc','Website','Internet','paid+social','Paid Social Media','Other values']
inquiry_source_detail_index=['Google','Direct Visit','facebook.com','Bing','Facebook','Other values']
group_oppurtunity_index=['Yes','No']
country_index=['United States of America','India','Nigeria','Canada','Mexico','Other values']
boas_self_apply_index=['Yes','No']
email_domain_index=['gmail.com','yahoo.com','hotmail.com','aol.com','icloud.com','Other values']



feature_names= ['Program_Type','ProgramSubType','UIAN','Inquiry_Source','Inquiry_Source_Detail','Group_Oppurtunity','Country','BOAS_Self_Appl','Email_Domain'] 
class FeaturesForm(FlaskForm):
    Program_Type=SelectField('Program_Type',[validators.DataRequired()],choices=[('Certificate','Certificate'),('Undergraduate','Undergraduate'),('Graduate','Graduate'),('None','None')])   
    ProgramSubType=SelectField('ProgramSubType',[validators.DataRequired()],choices=[('Pyschology','Psychology'),('Business','Business'),('Project Management','Project Management'),('Human Resourse & Leadership','Human Resourse & Leadership'),('Six Sigma','Six Sigma'),('Other values','Other values')])
    UIAN=SelectField('UIAN',[validators.DataRequired()],choices=[('Villanova University','Villanova University'),('Florida Institute of Technology','Florida Institute of Technology'),('Michigan State University','Michigan State University'),('New England College','New England College'),('University of Notre Dame','University of Notre Dame'),('Other values','Other values')])
    Inquiry_Source=SelectField('Inquiry_Souce',[validators.DataRequired()],choices=[('cpc','cpc'),('Website','Website'),('Internet','Internet'),('paid+social','paid+school'),('Paid Social Media','Paid Social Media'),('Other values','Other values')])
    Inquiry_Source_Detail=SelectField('Inquiry_Source_Detail',[validators.DataRequired()],choices=[('Google','Google'),('Direct Visit','Direct Visit'),('facebook.com','facebook.com'),('Bing','Bing'),('Facebook','Facebook'),('Other values','Other values')])
    Group_Oppurtunity=SelectField('Group_Oppurtunity',[validators.DataRequired()],choices=[('Yes','Yes'),('No','No')])
    Country=SelectField('Country',[validators.DataRequired()],choices=[('United States of America','United States of America'),('India','India'),('Nigeria','Nigeria'),('Canada','Canada'),('Mexico','Mexico'),('Other values','Other values')])
    BOAS_Self_Apply=SelectField('BOAS_Self_Apply',[validators.DataRequired()],choices=[('Yes','Yes'),('No','No')])
    Email_Domain=SelectField('Email_Domain',[validators.DataRequired()],choices=[('gmail.com','gmail.com'),('yahoo.com','yahoo.com'),('hotmail.com','hotmail.com'),('aol.com','aol.com'),('icloud.com','icloud.com'),('Other values','Other values')])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET','POST'])
def predict():
    form = FeaturesForm()
    if form.validate_on_submit():
        Program_Type=form.Program_Type.data
        Program_Type_val=program_type_index.index(Program_Type)
        ProgramSubType=form.ProgramSubType.data
        ProgramSubType_val=programsubtype_index.index(ProgramSubType)
        UIAN=form.UIAN.data
        UIAN_val=uian_index.index(UIAN)
        Inquiry_Source=form.Inquiry_Source.data
        Inquiry_Source_val=inquiry_source_index.index(Inquiry_Source)              
        Inquiry_Source_Detail=form.Inquiry_Source_Detail.data
        Inquiry_Source_Detail_val=inquiry_source_detail_index.index(Inquiry_Source_Detail)
        Group_Oppurtunity =form.Group_Oppurtunity.data
        Group_Oppurtunity_val=group_oppurtunity_index.index(Group_Oppurtunity)
        Country=form.Country.data
        Country_val=country_index.index(Country)
        BOAS_Self_Apply=form.BOAS_Self_Apply.data
        BOAS_Self_Apply_val=boas_self_apply_index.index(BOAS_Self_Apply)
        Email_Domain=form.Email_Domain.data 
        Email_Domain_val=email_domain_index.index(Email_Domain)
        features = [Program_Type,ProgramSubType,UIAN,Inquiry_Source,Inquiry_Source_Detail,Group_Oppurtunity,Country,BOAS_Self_Apply,Email_Domain]    
        features_val = [Program_Type_val,ProgramSubType_val,UIAN_val,Inquiry_Source_val,Inquiry_Source_Detail_val,Group_Oppurtunity_val,Country_val,BOAS_Self_Apply_val,Email_Domain_val] 
        df = pd.DataFrame([features], columns=feature_names)     
        prediction = model.predict([features_val])
        result = converted_index[prediction[0]]
        return render_template('result.html', df = df, result=result)
    return render_template('index.html', form=form)

class ImageForm(FlaskForm):
	image = FileField('Upload an image',validators=[FileAllowed(['jpg', 'png', 'jpeg'], u'Image only!'), FileRequired(u'File was empty!')])
	submit = SubmitField('Submit')

if __name__ == '__main__':
	app.run(debug=True)
