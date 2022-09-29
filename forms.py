"""Forms for playlist app."""
from wtforms.validators import InputRequired, Length, URL, Optional
from wtforms import SelectField, TextAreaField, StringField
from flask_wtf import FlaskForm


class PlaylistForm(FlaskForm):
    """Form for adding playlists."""
    name = StringField("Playlist Name", validators=[InputRequired(message="Playlist Name can't be blank")])
    description = TextAreaField("Content", validators=[InputRequired(message="Description required")]) 
    image_url = StringField("image_url", validators=[Optional(), URL(require_tld=True, message="Must be a url")])

class SongForm(FlaskForm):
    """Form for adding songs."""
    title = StringField("Title", validators=[InputRequired(message="Title is required"), Length(max=50)])
    artist = StringField("Artist", validators=[InputRequired(message="Artist is required"), Length(max=50)])

# DO NOT MODIFY THIS FORM - EVERYTHING YOU NEED IS HERE
class NewSongForPlaylistForm(FlaskForm):
    """Form for adding a song to playlist."""

    song = SelectField('Song To Add', coerce=int)
