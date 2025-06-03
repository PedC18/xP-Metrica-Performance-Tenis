from sportypy.surfaces.tennis import ATPCourt

def GetCourt(surface):
    court_params =  {
                "court_length": 78.0,
                "singles_width": 27.0,
                "court_units": "ft",
                "doubles_width": 36.0,
                "serviceline_distance": 21.0,
                "center_mark_length": 0.3333,
                "net_length": 36.0,
                "line_thickness": 0.3,
                "backstop_distance": 0.0,
                "sidestop_distance": 0.0
            }
    
    grass = {
        "plot_background": "white",
         "baseline": "#ffffff",
         "singles_sideline": "#ffffff",
         "doubles_sideline": "#ffffff",
         "serviceline": "#ffffff",
         "center_serviceline": "#ffffff",
         "center_mark": "#ffffff",
         "ad_court": "#9cb879",
         "deuce_court": "#9cb879",
         "backcourt": "#9cb879",
         "doubles_alley": "#9cb879",
         "court_apron": "#9cb879",
         "net": "#ffffff"
    }
    
    clay = {
        "plot_background": "white",
         "baseline": "#ffffff",
         "singles_sideline": "#ffffff",
         "doubles_sideline": "#ffffff",
         "serviceline": "#ffffff",
         "center_serviceline": "#ffffff",
         "center_mark": "#ffffff",
         "ad_court": "#a9765d",
         "deuce_court": "#a9765d",
         "backcourt": "#a9765d",
         "doubles_alley": "#a9765d",
         "court_apron": "#a9765d",
         "net": "#ffffff"
    }
    
    hard = {
        "plot_background": "white",
         "baseline": "#ffffff",
         "singles_sideline": "#ffffff",
         "doubles_sideline": "#ffffff",
         "serviceline": "#ffffff",
         "center_serviceline": "#ffffff",
         "center_mark": "#ffffff",
         "ad_court": "#3C638E",
         "deuce_court": "#3C638E",
         "backcourt": "#3C638E",
         "doubles_alley": "#3C638E",
         "court_apron": "#3C638E",
         "net": "#ffffff"
    }
    if surface == 'Grass':
        return ATPCourt(court_updates=court_params,color_updates=grass)
    elif surface == 'Hard':
        return ATPCourt(court_updates=court_params,color_updates=hard)
    elif surface == 'Clay':
        return ATPCourt(court_updates=court_params,color_updates=clay)
    else: 
        raise Exception("Sorry, no court with that surface. Choose between Clay, Grass or Hard")