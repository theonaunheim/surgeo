import surgeo

'''This is the basic model. Efficiency later.

   Where k is census block
   Where j is surname
   Where i is race (1 = Hispanic, 
                    2 = White, 
                    3 = Black, 
                    4 = Asian or Pacific Islander, 
                    5 = American Indian / Alaska Native, 
                    6 = Multiracial)

   Where u(i,j,k) = p(i|j) + r(k|i):

                                         u(i,j,k)
   q(i|j,k) = ---------------------------------------------------------------
              u(1,j,k) + u(2,j,k) + u(3,j,k) + u(4,j,k) + u(5,j,k) + u(6,j,k)
              
   What this means is better explained in the BACKGROUND.txt file.
'''

# Race dict for all functions
races = ['Hispanic', 
         'White', 
         'Black', 
         'Asian or Pacific Islander',
         'American Indian / Alaska Native', 
         'Multiracial']
# Index starts at 1 instead of zero
race_dict = { item[0] : item[1] for item in enumerate(races, start=1) }

def run_model(zcta, surname, db):
    '''Takes zcta, surname. Returns data percentages.
    
    Takes zip code, surname, and a database instance. Returns 6 separate 
    probabilities for each of the races above.
    
    For each (zcta, surname) pair, we must first get the probability for a 
    specific race is based on surname. We must then get get the probability for
    a specific race based on location. We then take prob_surname for that race
    and multiply it by prob_location. We multiply these together to get a 
    unified surname/geocode probability. We divide this probability by the
    probability of all the races together to give us our final probability. 
    Note that if there is no surname availible, fixed percentages are applied
    that should apply for all non-represented names. The numbers for this 
    particular statistic are fixed below, but the explanation is outside the 
    scope of this program. 
    '''
    #u(1,j,k) 
    prob_hispanic = get_combined_prob(1, zcta, surname, db)
    #u(2,j,k) 
    prob_white = get_combined_prob(2, zcta, surname, db)
    #u(3,j,k)
    prob_black = get_combined_prob(3, zcta, surname, db)
    #u(4,j,k)
    prob_api = get_combined_prob(4, zcta, surname, db)
    #u(5,j,k)
    prob_ai = get_combined_prob(5, zcta, surname, db)
    #u(6,j,k)
    prob_multi = get_combined_prob(6, zcta, surname, db)
    #denominator=u(1,j,k) + u(2,j,k) + u(3,j,k) + u(4,j,k) + u(5,j,k) + u(6,j,k)
    prob_combined = (prob_hispanic + 
                     prob_white + 
                     prob_black +
                     prob_api + 
                     prob_ai +
                     prob_multi)
    return surgeo.SurgeoResult(surname,
                               zcta,
                               '{0:f}'.format(prob_hispanic/prob_combined),
                               '{0:f}'.format(prob_white/prob_combined),
                               '{0:f}'.format(prob_black/prob_combined),
                               '{0:f}'.format(prob_api/prob_combined),
                               '{0:f}'.format(prob_ai/prob_combined),
                               '{0:f}'.format(prob_multi/prob_combined))
        
def get_combined_prob(race,
                      zcta,
                      surname,
                      db):
    '''This gets combined probability: u(i,j,k)'''
    surname_prob = get_prob_surname(race, surname, db)
    zcta_prob = get_prob_zcta(race, zcta, db)
    combined_prob = surname_prob * zcta_prob
    return combined_prob

def get_prob_surname(race,
                     surname,
                     db):
    '''This gets probability of surname: p(i|j)'''
    cursor = db.cursor()
    cursor.execute('''SELECT pcthispanic, pctwhite, pctblack, pctapi,
                      pctaian, pct2prace FROM surname_data WHERE name=?''',
                      (surname,))
    fetched = cursor.fetchone()
    try:
        # csv in percentage form
        hispanic = fetched[0]/100
        white = fetched[1]/100
        black = fetched[2]/100
        api = fetched[3]/100
        ai = fetched[4]/100
        multiracial = fetched[5]/100
    except TypeError:
        # If not in database (nonetype returned), fixed percentages from study
        hispanic = float(11.1)/100
        white = float(70.5)/100
        black = float(11.3)/100
        api = float(7.0)/100
        ai = float(.9)/100
        multiracial = float(.8)/100
    # Sync race with probability
    prob_index = { 1 : hispanic, 
                   2 : white, 
                   3 : black, 
                   4 : api, 
                   5 : ai, 
                   6 : multiracial }
    return prob_index[race]
        
def get_prob_zcta(race,
                  zcta,
                  db):
    '''This gets probability of zcta: r(k|i).'''
    # Add up all the blocks in the zip.
    cursor = db.cursor()
    count_hispanic = 0
    count_white = 0
    count_black = 0
    count_api = 0
    count_ai = 0
    count_multi = 0
    # First select a list of logical records for a given zip
    cursor.execute('''SELECT state, logical_record FROM 
                      geocode_data WHERE zcta=?''', (zcta,))
    state, logical_record = cursor.fetchone()
    # For each of the results, get race results for logical record
    # Each state will likely have a logical record with that number, filter
    # State 
    cursor.execute('''SELECT num_hispanic, num_white, num_black, 
                      num_api, num_ai, num_multi FROM logical_race_data 
                      WHERE logical_record=? AND state=?''', 
                      (logical_record, state))
    row = cursor.fetchone()
    # hispanic, white, black, api, indian, multirace.
    count_hispanic = row[0]
    count_white = row[1]
    count_black = row[2]
    count_api = row[3]
    count_ai = row[4]
    count_multi = row[5]
    # total should come from data pop, not adding components together
    total = (count_hispanic + count_white + count_black + count_api +
             count_ai + count_multi)
    hispanic = count_hispanic / total
    white = count_white / total
    black = count_black / total
    api = count_api / total
    ai = count_ai / total
    multiracial = count_multi / total
    # Sync race with probability
    prob_index = { 1 : hispanic, 
                   2 : white, 
                   3 : black, 
                   4 : api, 
                   5 : ai, 
                   6 : multiracial }
    return prob_index[race]
    


                          
    
    
                                 
                                 


