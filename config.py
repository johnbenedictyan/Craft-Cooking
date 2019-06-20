import os
FLASKS3_BUCKET_NAME = os.environ.get("FLASKS3_BUCKET_NAME")
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_SECRET_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
FLASKS3_HEADERS = {'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT','CacheControl': 'max-age=9460800'}
FLASKS3_GZIP = 'True'
UPLOAD_LOCATION =  'http://{}.s3.amazonaws.com/'.format(FLASKS3_BUCKET_NAME)
ALLOWED_FILE_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
PROFILE_PICTURE_LOCATION = "http://{}.s3.amazonaws.com/uploads/profile-pictures/".format(FLASKS3_BUCKET_NAME)
RECIPE_PICTURE_LOCATION = "http://{}.s3.amazonaws.com/uploads/recipe-pictures/".format(FLASKS3_BUCKET_NAME)
SQLALCHEMY_DATABASE_URI = "sqlite:///example.sqlite"
SQLALCHEMY_TRACK_MODIFICATIONS = "False"
PERMANENT_SESSION_LIFETIME = 1800
