from django.urls import path
from . import views 

urlpatterns = [
    path('',views.HomeView.as_view(),name="home"), #Page
    path('create-post/',views.CreatePostView.as_view(),name="create-post"), #Page
    path('request-cor/<int:pk>/',views.RequestCorApplicaiton.as_view(),name="request-cor"), #Hx
    path('request-gm/<int:pk>/',views.RequestGMApplicaiton.as_view(),name="request-gm"), #Hx
    path('select-cor/<int:pk>/<int:pk_cor>/',views.SelectCorView.as_view(),name="select-cor"),
    path('select-gm/<int:pk>/<int:pk_gm>/',views.SelectGMView.as_view(),name="select-gm"),
    # Team Management for Cordinator
    path('team-manager/<int:pk>/',views.TeamManagerView.as_view(),name="team-manager"),
    path('team-list/<int:pk>/',views.ViewTeamList.as_view(),name="team-list"),
    path('team-create/<int:pk>/',views.TeamCreateView.as_view(),name="team-create"),
    path('team-detail/<int:pk>/<int:pk_team>/',views.TeamDetailView.as_view(),name="team-detail"),
    path('team-update/<int:pk>/<int:pk_team>/',views.TeamUpdateView.as_view(),name="team-update"),
    path('team-delete/<int:pk>/<int:pk_team>/',views.TeamDeleteView.as_view(),name="team-delete"),

    path('player-create/<int:pk>/',views.PlayerCreateView.as_view(),name="player-create"),
    path('player-update/<int:pk>/<int:pk_player>/',views.CorUpdatePlayer.as_view(),name="player-update"),
    path('gm-player-update/<int:pk>/<int:pk_player>/',views.GMUpdatePlayer.as_view(),name="gm-player-update"),
    path('player-delete/<int:pk>/<int:pk_player>/',views.CorDeletePlayer.as_view(),name="player-delete"),
    # Match Management_for Game manager
    path('match-manager/<int:pk>/',views.MatchManagerView.as_view(),name="match-manager"),
    path('match-list/<int:pk>/',views.ViewMatchList.as_view(),name="match-list"),
    path('match-create/<int:pk>/',views.MatchCreateView.as_view(),name="match-create"),
    path('match-update/<int:pk>/<int:pk_match>/',views.MatchUpdateView.as_view(),name="match-update"),
    path('match-detail/<int:pk>/<int:pk_match>/',views.MatchDetailView.as_view(),name="match-detail"),
    # Tie-sheet Generation in excel file
    path('tie-sheet/', views.tie_sheet, name='tie-sheet'),
]
