from django.db import connection

query = """
    do $$
        declare
            _imported_member record;
            _user_id int;
            _scheme_group_id int;
            _membership_id int;
            _policy_id int;
            _individual_user_id int;
            _policy_holder_id int;
            _sa_id_is_valid bool;
            _user_age_is_valid bool;
            _user_geder text;
            _user_date_of_birth text;
            _user_pricing_plan text;
            _product_id int;
            _user_identification_method text;
            _premium decimal;
            _cycle_id int;
        begin
            -- get the product id from the first row
            select product into _product_id from sales_temporarymemberdata limit 1;

            -- create synergy scheme group
            INSERT INTO schemes_schemegroup (created,modified,scheme_id,description,name,payment_method,period_frequency,period_type,pricing_group,cycle_type) 
            VALUES (now(),now(),2,get_pricing_plan(_product_id),get_pricing_plan_updated(_product_id),'debit_order',1,'MONTH',get_pricing_plan_updated(_product_id),'MEMBER_CYCLE')
            RETURNING id INTO _scheme_group_id;

            INSERT INTO policies_policy(created,modified,policy_number,amount,start_date,payment_due_day,payment_frequency,status,terms_and_conditions_accepted,claim_lodging_awaiting_period,insurance_product_id,creator_id,proxy_purchase,is_group_policy,dg_required,config,policy_number_counter,policy_document,welcome_letter)
            VALUES (now(),now(),CONCAT(get_policy_number_prefix_updated(_product_id),_scheme_group_id),0,TO_CHAR(now(), 'yyyy-mm-01')::date,2,'monthly','active',true,0,1,_user_id,'false','false','true','{}',1,'','')
            RETURNING id INTO _policy_id;

            -- create entry in policy details table
            INSERT INTO policy_details(created,modified,extra_premium,policy_id,funeral_policy_details,activation_details)
            VALUES (now(),now(),0,_policy_id,'{}','{}');


            UPDATE schemes_schemegroup
            SET policy_id = _policy_id
            where id = _scheme_group_id;

        FOR _imported_member in select * from member_import
            LOOP
                raise notice 'counter: %',concat('member ', _imported_member.member_import_username);
                -- first check the identification method and assign variables
                _user_pricing_plan := get_pricing_plan_updated(_product_id);
                _user_identification_method := get_identification_method(_imported_member.member_import_identification_method);
                if _user_identification_method = 'South African ID' and validate_age(_imported_member.member_import_identification_number) = true and id_is_valid(_imported_member.member_import_identification_number) = true then
                    _user_geder := get_gender(_imported_member.member_import_identification_number);
                    _user_date_of_birth := get_date_of_bith(_imported_member.member_import_identification_number);
                else
                    _user_geder := _imported_member.member_import_gender;
                    _user_date_of_birth := _imported_member.member_import_date_of_birth;
                end if;


                -- check if the user already exists 
                IF EXISTS (select * from users_profile where id_number = _imported_member.member_import_identification_number) then
                    raise notice 'User exists';
                    -- get the user id
                    select user_id into _user_id from users_profile where id_number = _imported_member.member_import_identification_number;
                    -- get individual user id
                    select id into _individual_user_id from users_individualuser where user_id = _user_id;
                    -- get policy holder id 
                    select id into _policy_holder_id from users_policyholder where individual_user_id = _user_id;
                ELSE
                    raise notice 'User does notexists';
                    -- create user
                    INSERT INTO users_user (password,is_superuser,username,first_name,last_name,is_staff,is_active,date_joined,created,modified,email,role,sent_emails,reset_password)
                    VALUES ('temp_password',false,_imported_member.member_import_username,_imported_member.member_import_first_name,_imported_member.member_import_last_name,false,true,now(),now(),now(),_imported_member.member_import_email,'individual',0,false)
                    RETURNING id INTO _user_id;


                    -- create user profile
                    if _user_identification_method = 'South African ID' then
                        INSERT INTO users_profile(created,modified,user_id,first_name,last_name,id_number,date_of_birth,gender,address,phone,address1,phone1)
                        VALUES(now(),now(),_user_id,_imported_member.member_import_first_name,_imported_member.member_import_last_name,_imported_member.member_import_identification_number,DATE(_user_date_of_birth),_user_geder,_imported_member.member_import_physical_address,_imported_member.member_import_mobile_number,'','');
                    else
                        INSERT INTO users_profile(created,modified,user_id,first_name,last_name,passport_number,date_of_birth,gender,address,phone,address1,phone1)
                        VALUES(now(),now(),_user_id,_imported_member.member_import_first_name,_imported_member.member_import_last_name,_imported_member.member_import_identification_number,DATE(_imported_member.member_import_date_of_birth),_imported_member.member_import_gender,_imported_member.member_import_physical_address,_imported_member.member_import_mobile_number,'','');
                    end if;

                    -- create individual user
                    INSERT INTO users_individualuser (user_id)
                    VALUES (_user_id)
                    RETURNING id INTO _individual_user_id;


                    -- create policy holder using S.A if provided
                    -- if not passport
                    if _user_identification_method = 'South African ID' then
                        INSERT INTO users_policyholder(name,address,phone_number,id_number,individual_user_id,date_of_birth,gender,address1,phone,phone1)
                        VALUES (_imported_member.member_import_first_name,_imported_member.member_import_physical_address,_imported_member.member_import_mobile_number,_imported_member.member_import_identification_number,_individual_user_id,DATE(_user_date_of_birth),_user_geder,_imported_member.member_import_physical_address,_imported_member.member_import_mobile_number,_imported_member.member_import_landline)
                        RETURNING id INTO _policy_holder_id;
                    else
                        INSERT INTO users_policyholder(name,address,phone_number,passport_number,individual_user_id,date_of_birth,gender,address1,phone,phone1)
                        VALUES (_imported_member.member_import_first_name,_imported_member.member_import_physical_address,_imported_member.member_import_mobile_number,_imported_member.member_import_identification_number,_individual_user_id,DATE(_imported_member.member_import_date_of_birth),_imported_member.member_import_gender,_imported_member.member_import_physical_address,_imported_member.member_import_mobile_number,_imported_member.member_import_landline)
                        RETURNING id INTO _policy_holder_id;
                    end if;
                END IF;
                    
                        
                -- create membership
                INSERT INTO users_membership(created,modified,user_id,scheme_group_id,member_id,properties)
                VALUES (now(),now(),_user_id,_scheme_group_id,gen_random_uuid(),'{}')
                RETURNING id INTO _membership_id;

                --create cycle
                INSERT INTO policies_cycle(created,modified,membership_id,scheme_group_id, status)
                VALUES (now(),now(),_membership_id, _scheme_group_id, 'active')
                RETURNING id INTO _cycle_id;

                --create cycle status update
                INSERT INTO policies_cyclestatusupdates(created,modified,cycle_id,previous_status,next_status)
                VALUES(now(),now(),_cycle_id,'awaiting_payment','active');
                
                -- create membership config
                INSERT INTO users_membershipconfiguration(created,modified,membership_id,cover_level)
                VALUES (now(),now(),_membership_id,5000);		


                -- create unpdaid payment records
                INSERT into payments_policypremium(created,modified,balance,expected_payment,expected_date,status,policy_id,detailed_balance,payments_details,membership_id,retry_status)
                VALUES(now(),now(),0,get_premium_amount(_user_pricing_plan),now(),'paid',_policy_id,'{}','{}',_membership_id,'Unknown');
                
                INSERT into payments_policypayment(created,modified,premium,vat,state,type,payment_due_date,policy_id,extra_premium,membership_id)
                values(now(),now(),get_premium_amount(_user_pricing_plan),0,'SUCCESSFUL','Debit Order',now(),_policy_id,0,_membership_id);
            END LOOP;

        end; $$
"""
