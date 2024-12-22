# 241110_instagram_profiles_affinity
Building a search engine for influencers. 

## To-do list
- [x] ~~Implement `discriminator_agent` for conversational ability~~
- [x] ~~Implement `GooperModel` class~~
- [ ] Implement `feedback_agent` to provide feedback when invalid input
- [ ] Convert from client calls to API calls
- [x] ~~Migrate Influencer Database to Supabase~~
- [ ] Scale database to 100,000 influencers
- [ ] embed profile summary directly (bypass description generation)
- [x] ~~Implement model API for custom deployment~~

## Release History
| Version | Changes | Status |
|---------|---------|--------|
| 1.1.3     | Scale up the database to 90 influencers     | Online     |
| 1.1.2     | Implement a discriminator agent to improve conversational ability     | -     |
| 1.1.1     | Re-organize the model in a single class    | -     |
| 1.1.0     | Migrate Influencer Database to Supabase     | -     |
| 1.0.0     | Initial Deployment on Streamlit Cloud     | -     |

## Resources
- [Supabase Docs](https://supabase.com/docs/reference/python/introduction)
- [Supabse Project](https://supabase.com/dashboard/project/edcqmzluacqdqqmmklik)
- [pgvector](https://github.com/pgvector/pgvector)

## Commands
```
mkvirtualenv myenv --python=python3.10
workon myenv
```