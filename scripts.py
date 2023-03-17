scriptall ='''
                select distinct
                    w.id_ot, w.num_ticket, nd.name_nap, nd.issue, nd.fase, nd.coord, dt.date_demand, 
                    w.affect_clients, datediff(now(), dt.date_demand), st.priority, cw.partner_name, 
                    cw.group_name, zd.name_dep, zd.name_city, zd.name_district, st.state_order,
                    dt.date_done, st.reason, st.down_users
                from 
                    work w, nap_desc nd, status st, date dt, crew cw, zone_desc zd
                where 
                    w.id_ot = nd.id_ot
            '''

scriptRowCount = '''
                    select 
                        COUNT(*)
                    from 
                        work
                '''