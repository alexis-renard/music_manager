from .app import db, login_manager, app
from flask.ext.login import UserMixin
from wtforms import StringField, HiddenField, PasswordField, SelectField, RadioField, validators
from wtforms.validators import DataRequired, Required, EqualTo, Length
from flask.ext.wtf import Form
from hashlib import sha256
from flask.ext.login import login_user, current_user, logout_user, login_required



#Création de la table belong entre album et Genre
belong = db.Table('belong',
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'), nullable=False),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), nullable=False),
    db.PrimaryKeyConstraint('album_id', 'genre_id')
)

belong_playlist_album = db.Table('belong_playlist_album',
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'), nullable=False),
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), nullable=False),
    db.PrimaryKeyConstraint('album_id', 'playlist_id')
)

#Création de la table Artist
class Artist(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100))

    def __repr__(self):
        return "<Artist (%d) %s>" % (self.id, self.name)

    def get_id_a(self):
        return self.id

    def get_name(self):
        return self.name


#Création de la table Genre
class Genre(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    name_g       = db.Column(db.String(100))

    def __repr__(self):
        return "<Genre (%d) %s>" % (self.id, self.name_g)

    def get_id_g(self):
        return self.id

    def get_name_g(self):
        return self.name_g

class Compositor(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100))

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

class Playlist(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100))
    visibility  = db.Column(db.Boolean)
    user_name   = db.Column(db.Integer, db.ForeignKey("user.username"))
    user        = db.relationship("User", backref = db.backref("playlists", lazy="dynamic"))
    albums      = db.relationship("Album", secondary=belong_playlist_album, backref = db.backref("playlists", lazy="dynamic"))

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_visibility(self):
        return self.visibility


#Création de la table Ablum
class Album(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    title           = db.Column(db.String(100))
    releaseYear     = db.Column(db.String(100))
    img             = db.Column(db.String(100))
    compositor_id   = db.Column(db.Integer, db.ForeignKey("compositor.id"))
    artist_id       = db.Column(db.Integer, db.ForeignKey("artist.id"))
    artist          = db.relationship("Artist", backref = db.backref("albums", lazy="dynamic"))
    genres          = db.relationship("Genre", secondary=belong, backref = db.backref("albums", lazy="dynamic"))

    def __repr__(self):
        return "<Album (%d) %s>" % (self.id, self.title)

    def get_id_al(self):
        return self.id

    def get_title(self):
        return self.title

    def get_compositor(self):
        return self.compositor_id

    def get_releaseYear(self):
        return self.releaseYear

    def get_img(self):
        return self.img

    def get_artist_id(self):
        return self.artist_id

    def get_genres(self):
        return self.genres

#Création de la table User
class User(db.Model, UserMixin):
    username        = db.Column(db.String(50), primary_key=True)
    password        = db.Column(db.String(64))
    admin           = db.Column(db.Boolean)

    def get_id(self):
        return self.username

class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])

class ArtistForm(Form):
	id			= HiddenField('id')
	name		= StringField('Nom', validators=[DataRequired()])

class GenreForm(Form):
	id			= HiddenField('id')
	name_g		= StringField('Nom Genre', validators=[DataRequired()])

class AlbumForm(Form):
    id			= HiddenField('id', validators=[DataRequired()])
    title		= StringField('Titre Album', validators=[DataRequired()])
    releaseYear	= StringField('Année de sortie', validators=[DataRequired()])

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4), validators.Required()]) #ce qui est entre simple quote correspond au label du champs
    password = PasswordField('Password', [validators.Length(min=4), validators.Required()])
    next = HiddenField()

    def get_authenticated_user(self):
        user = User.query.get(self.username.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password else None

class PlaylistForm(Form):
    id			= HiddenField('id', validators=[DataRequired()])
    name        = StringField('Nom de la playlist', validators=[DataRequired()])
    visibility  = SelectField(
                        'Visibilité',
                        choices=[('1','Publique'), ('0','Privée')],
                        default='1'
                  )

class PlaylistFormCreate(Form):
    id			= HiddenField('id', validators=[DataRequired()])
    name        = StringField('Nom de la playlist', validators=[DataRequired()])

class RegisterForm(Form):
	username = StringField('Username', [validators.Length(min=4), validators.Required()])
	password = PasswordField('Password', [
		validators.Required(),
		validators.EqualTo('confirm', message='Passwords must match'),
        validators.Length(min=4)
	])
	confirm = PasswordField('Repeat Password', [validators.Length(min=4), validators.Required()])
	next = HiddenField()

##### Fonctions Artist ####

def get_all_artists():
    return Artist.query.all()

def get_artist(id):
    return Artist.query.get(id)


def get_all_albums():
    return Album.query.all()

def get_all_genres():
    return Genre.query.all()

def get_all_playlists():
    return Playlist.query.all()


def get_album(id):
    return Album.query.get(id)

def get_genre(id):
    return Genre.query.get(id)

def get_playlist(id):
    return Playlist.query.get(id)

def get_user(username):
    return User.query.get(username)

def get_admin(admin):
    return User.query.get(admin)

def get_playlists_user(username):
    return User.query.get(username).playlists

def get_public_playlists():
    return Playlist.query.filter(Playlist.visibility==1).all()

def get_private_playlists():
    return Playlist.query.filter(Playlist.visibility==0).all()


## PEUT ÊTRE A SUPPRIMER CAR ON PEUT UTILISER DIRECTEMENT LES BACKREFS

def get_private_playlists_user(username):
    listePlaylist = set()
    for playlist in get_playlists_user(username):
        if not playlist.visibility :
            listePlaylist.add(playlist)
    return listePlaylist

def get_public_playlists_user(username):
    listePlaylist = set()
    for playlist in get_playlists_user(username):
        if playlist.visibility :
            listePlaylist.add(playlist)
    return listePlaylist

## FIN PEUT ÊTRE A SUPPRIMER CAR ON PEUT UTILISER DIRECTEMENT LES BACKREFS


def get_sample_public_playlists():
    playlists = get_playlists()
    listePlaylist = set()
    cpt = 0
    #implémenter un while ici
    for playlist in playlists:
        if playlist.visibility and cpt < 3:
            listePlaylist.add(playlist)
            cpt+=1
    return listePlaylist


def get_sample_playlist_user(username):
    playlists = get_playlists_user(username)
    listePlaylist = set()
    cpt = 0
    #implémenter un while ici
    for playlist in playlists:
        if cpt < 2:
            listePlaylist.add(playlist)
            cpt+=1
    return listePlaylist

def get_genre_playlist_user(username):
    playlists = get_playlists_user(username)
    listeGenre = set()
    for playlist in playlists:
        for album in playlist.albums:
            for genre in album.genres:
                listeGenre.add(genre)
    return listeGenre

def get_albums_artist(idartist):
    # return Album.query.filter(Album.artist_id==idartist).all()
    return Artist.query.get(idartist).albums

def get_all_album_playlist_user(username):
    playlists = get_playlists_user(username)
    listeAlbums = set()
    for playlist in playlists:
        for album in playlist.albums:
            listeAlbums.add(album)
    return listeAlbums

def get_albums_playlist(idplaylist):
    return Playlist.query.get(idplaylist).albums

def get_albums_genre(idgenre):
    return Genre.albums

def get_artists_genre(idgenre):
    return Artist.query.filter(Album.genres.any(id=idgenre)).all()

def get_playlistByNameUser(name, username):
    playlists = get_playlists_user(username)
    listePlaylist = set()
    for playlist in playlists:
        if playlist.name == name:
            listePlaylist.add(playlist)
    return listePlaylist

def get_playlist_sans_doublons(idalbum,username):
    playlists = get_playlists_user(username)
    listePlaylist = set()
    for playlist in playlists:
        contenu = False
        for album in playlist.albums:
            if album.id==idalbum:
                contenu = True
        if not contenu :
            listePlaylist.add(playlist) #si on n'a pas l'album dans la playlist, alors on peut la choisir pour y ajouter notre album
    return(listePlaylist)

def get_genre(name_g):
    return Genre.query.get(name_g)

def get_compositor(id):
    return Compositor.query.get(id)

def get_sample_albums():
    return Album.query.limit(8).all()

def get_sample_genre():
    return Genre.query.limit(3).all()

def get_sample_artists():
    return Artist.query.limit(5).all()

def get_artist_search(search):
    return Artist.query.filter(Artist.name.like("%"+search+"%")).all()

def get_album_search_title(search):
    return Album.query.filter(Album.title.like("%"+search+"%")).all()

def get_compositor_search(search):
    return Compositor.query.filter(Compositor.name.like("%"+search+"%")).all()

def get_album_search_releaseYear(search):
    return Album.query.filter(Album.releaseYear.like("%"+search+"%")).all()

def get_album_search_playlist(search):
    return Playlist.query.filter(Playlist.name.like("%"+search+"%")).all()

def get_album_search_playlist_username(search,username):
    playlists = get_album_search_playlist(search)
    dicoPlaylist = {'publique':set(),'privee':set()}
    for playlist in playlists:
        if playlist.visibility == 1:
            dicoPlaylist['publique'].add(playlist)
        if playlist.user_name == username:
            dicoPlaylist['privee'].add(playlist)
    return dicoPlaylist

def get_genre_search(search):
    return Genre.query.filter(Genre.name_g==search).all()

def get_date_albums(releaseY):
    return Album.query.filter(Album.releaseYear==releaseY).all()

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

@app.context_processor
def utility_processor():
    def get_name_compositor_context(idcompositor):
        return get_compositor(idcompositor).get_name()
    def get_name_artist_context(idartist):
        return get_artist(idartist).get_name()
    return dict(get_name_compositor_context=get_name_compositor_context,get_name_artist_context=get_name_artist_context)
