"""Models for Playlist app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRpDuBw1Pgtaa_qELB_2wzkGcVMF1fuL9K8Q&usqp=CAU"

class Playlist(db.Model):
    """Playlist."""

    __tablename__ = 'playlists' 

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.Text, nullable=True, default=DEFAULT_IMAGE_URL)

    def __repr__(self): 
        p = self
        return f"<Playlist id={self.id} name={p.name} description={p.description} image_url={p.image_url}>" 

class Song(db.Model):
    """Song."""

    __tablename__ = 'songs' 

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False, unique=True)
    artist = db.Column(db.Text, nullable=False)
    
    playlists = db.relationship('Playlist', secondary="playlists_songs", backref="songs", cascade="all,delete") 

    def __repr__(self): 
        s = self
        return f"<Song id={self.id} title={s.title} artist={s.artist}>" 

class PlaylistSong(db.Model):
    """Mapping of a playlist to a song."""

    __tablename__ = 'playlists_songs' 

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), primary_key=True)

    def __repr__(self): 
        ps = self
        return f"<PlaylistSong id={self.id} playlist_id={ps.playlist_id} song_id={ps.song_id}>" 

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
