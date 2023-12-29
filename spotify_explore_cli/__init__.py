import random
from typing_extensions import Annotated

import typer
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from rich import print as rprint
from rich.progress import Progress
from rich.panel import Panel

app = typer.Typer()


@app.command("get_random_artists")
def get_random_artists(
    artists_number: Annotated[
        int, typer.Option("-n")
    ] = 3
):
    # python -m spotify_explore_cli get_random_artists
    # set open_browser=False to prevent Spotipy from attempting to open the default browser
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-follow-read"))
    artists = get_all_artists(spotify)
    print(f"Found {len(artists)} artists")
    random.shuffle(artists)

    for artist in artists[:artists_number]:
        panel = Panel(
            artist["external_urls"]["spotify"], 
            title=f'{artist["name"]}: {artist["followers"]["total"]}', 
            subtitle=", ".join(artist["genres"]),
            width=100
        )
        rprint(panel)


def get_all_artists(spotify):
    response = spotify.current_user_followed_artists(limit=50)
    after = response["artists"]["cursors"]["after"]
    total = response["artists"]["total"]
    artists = response["artists"]["items"]

    with Progress() as progress:
        load_artists_task = progress.add_task("[red]Loading artists...", total=total)    
        while len(artists) < total:
            response = spotify.current_user_followed_artists(limit=50, after=after)
            after = response["artists"]["cursors"]["after"]
            artists += response["artists"]["items"]
            progress.update(load_artists_task, advance=len(response["artists"]["items"]))

    return artists



@app.command()
def test():
    # python -m spotify_explore_cli test
    pass



def build_auth_url(additional_scopes=[], client_id='b31dfb19b7864c0da1a925332c48c074'):
    """Create the OAuth URL for the user-approved scopes."""
    user_scopes = ['Read & modify playback.'] + additional_scopes
    scopes = []
    for scope in AUTH_SCOPES_MAPPING:
        if scope['name'] in user_scopes:
            scopes += scope['scopes']

    auth_url = (
        'https://accounts.spotify.com/authorize?client_id={}'
        '&response_type=code&redirect_uri={}&scope={}&state={}'
        .format(
            client_id,
            ul.quote_plus(REDIRECT_URI),
            ul.quote_plus(" ".join(scopes)),
            uuid1(),
        )
    )
    return auth_url
