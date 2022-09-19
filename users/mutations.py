import graphene

class UserRegisterMutation(graphene.Mutation):
    user = graphene.Field(UserType)
    success = graphene.Boolean()
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        name = graphene.String(required=True)
        password = graphene.String(required=True)
        password_confirmation = graphene.String(required=True)
        role_id = graphene.Int()
        language = graphene.String(required=True)
        partner = graphene.Int()
        country_code = graphene.String()
        timezone = graphene.String()
        facebook_link = graphene.String()
        twitter_link = graphene.String()
        customer_key = graphene.String()

    @staticmethod
    def mutate(self, info,
               email=None, name=None, password=None,
               password_confirmation=None, role_id=None, language=None,
               partner=None, country_code=None, timezone=None,
               facebook_link=None, twitter_link=None, customer_key=None):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            raise Exception('User already exists!')
        elif password != password_confirmation:
            raise Exception('Passwords do not match!')
        else:
            partner = partner if partner else None
            country_code = country_code if country_code else 'DK'
            timezone = timezone if timezone else 'Europe/Copenhagen'
            customer_key = customer_key if customer_key else name.lower().replace(" ", "-") + str(
                random.randint(1111, 9999))

            country_instance = Countries.objects.get(code=country_code)
            timezone_instance = Timezones.objects.get(zone_name=timezone)

            role_id = role_id if role_id else 3

            user_instance = User(name=name, email=email, timezone=timezone_instance,
                                 country_code=country_instance, partner=partner, lang=language,
                                 customer_key=customer_key, facebook_link=facebook_link,
                                 twitter_link=twitter_link)

            user_instance.set_password(password_confirmation)
            user_instance.is_active = True
            user_instance.is_staff = False
            user_instance.save()

            user_role = UserRoles(user_id=user_instance.id, role_id=role_id)
            user_role.save()

            token = get_token(user_instance)
            refresh_token = create_refresh_token(user_instance)

            return UserRegisterMutation(user=user_instance,
                                        success=True,
                                        token=token,
                                        refresh_token=refresh_token
                                        )