from flask import Flask, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def root():
    """Homepage: redirect to /playlists."""

    return redirect("/playlists")


##############################################################################
# Playlist routes


@app.route("/playlists")
def show_all_playlists():
    """Return a list of playlists."""

    playlists = Playlist.query.all()
    return render_template("playlists.html", playlists=playlists)


@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show detail on specific playlist."""

    playlist = Playlist.query.get(playlist_id)
    songs = playlist.songs
    return render_template('playlist.html', playlist=playlist, songs=songs)

@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    """Handle add-playlist form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-playlists
    """
    form = PlaylistForm()
    if form.validate_on_submit():

        name = form.name.data
        description = form.description.data
        image_url = form.image_url.data
       
        new_playlist = Playlist(name=name, description=description, image_url=image_url)
        db.session.add(new_playlist)

        try:
            db.session.commit()
        except IntegrityError:
            form.name.errors.append('Name taken.  Please pick another')
            return render_template('new_playlist.html', form=form)
        flash(f'Welcome! You Have Created a New Playlist, {new_playlist.name}!', "success")
        return redirect('/playlists')

    return render_template('new_playlist.html', form=form)

##############################################################################
# Song routes


@app.route("/songs")
def show_all_songs():
    """Show list of songs."""

    songs = Song.query.all()
    return render_template("songs.html", songs=songs)


@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """return a specific song"""
    song = Song.query.get(song_id)
    playlists = song.playlists
    return render_template('song.html', song=song, playlists=playlists)

@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    """Handle add-song form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-songs
    """
    form = SongForm()

    if form.validate_on_submit():

        title = form.title.data
        artist = form.artist.data

        new_song = Song(title=title, artist=artist)
        db.session.add(new_song) 

        try:
            db.session.commit()
        except IntegrityError:
            form.title.errors.append('Title taken.  Please pick another')
            return render_template('new_playlist.html', form=form)
        flash(f'Welcome! You Have Added a New Song, {new_song.title}!', "success")
        return redirect('/songs')
    return render_template("new_song.html", form=form)


@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a playlist and redirect to list."""

    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()

    # Restrict form to songs not already on this playlist

    curr_on_playlist = [s.id for s in playlist.songs]
    form.song.choices = (db.session.query(Song.id, Song.title)
                      .filter(Song.id.notin_(curr_on_playlist))
                      .all())

    if form.validate_on_submit():

        song_id = form.song.data
        song = Song.query.get(song_id)
        new_playlist_song = PlaylistSong(playlist_id=playlist_id, song_id=song_id)
        db.session.add(new_playlist_song) 

        try:
            db.session.commit()
        except IntegrityError:
            form.title.errors.append('Title already on playlist.  Please pick another')
            return render_template('add_song_to_playlist.html', playlist=playlist, form=form)
        flash(f'Welcome! You Have Added a New Song to a Playlist, {song.title}!', "success")

        return redirect(f"/playlists/{playlist_id}")

    return render_template("add_song_to_playlist.html",
                             playlist=playlist,
                             form=form)
