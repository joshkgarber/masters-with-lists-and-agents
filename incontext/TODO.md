# TODO

- [x] Only admin can manage master lists
- [x] Admin can manage all admin-created master lists and master agents
- [x] Master list and master agent views show the creator name
- [x] You can create a (tethered) list off a master as a copy which you can add items to.
- [ ] You cannot edit the name, descriptions, items or details from the master list
    - Currently you can create a tethered list, and there is no link to edit it.
    - You can, however get to the edit form to edit the name and description via the url.
    - Need to block requests for the edit route for lists which are tethered lists.
    - That has now been blocked. Now I need to check whether you can edit the master list items.
    - I found that it's showing the items in the wrong place and not showing the details.
    - I fixed it. The items are in the right place now.
    - It's not showing the details from master.
    - I fixed it. It's now showing the details from master.
- [ ] You can add items to list
- [ ] You cannot add details to a tethered list
- [ ] The data is not duplicated. The tethered list is concatenated to the master list when served.
