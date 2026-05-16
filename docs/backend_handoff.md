# Backend Handoff: Favorites, Bids, and Finalization

Use these backend-provided variables and URL names when updating templates. Do not hard-code paths; keep using Django `{% url %}` tags with the `marketplace` namespace.

## Favorites

- `marketplace:toggle_favorite` expects `POST` at `artworks/<pk>/favorite/`.
- Favorite forms should include `{% csrf_token %}` and may include `<input type="hidden" name="next" value="{{ request.get_full_path }}">` so the backend redirects back to the current page.
- `home.html` receives `latest_artworks` and `favorite_artwork_ids`.
- `artwork_list.html` receives `page_obj`, `mediums`, `styles`, `filters`, and `favorite_artwork_ids`. Use `artwork.pk in favorite_artwork_ids` for saved-state UI.
- `artwork_detail.html` receives `artwork`, `existing_bid`, and `is_favorite`. Use `is_favorite` for the detail-page saved-state UI.
- `favorite_list.html` receives `artworks` and `favorite_artwork_ids`. The list is already filtered to the logged-in user's favorites.
- Favorites routes are login-protected where they mutate or show user-specific data. Anonymous users should be linked to `marketplace:login` with an appropriate `next` query string.

## Bids

- `marketplace:submit_bid` supports bid create/update at `artworks/<pk>/bid/`.
- `bid_form.html` receives `artwork`, `form`, and `existing_bid`. If `existing_bid` is present, the form edits/resubmits that user's bid for the artwork.
- `artwork_detail.html` receives `existing_bid`; use it to switch between "Submit a bid" and "Resubmit a bid" and to display current bid status.
- `marketplace:bid_list` renders `bid_list.html` with `bids`, ordered newest first and scoped to the logged-in user.
- `bid_list.html` should use `bid.artwork`, `bid.artwork.seller`, `bid.created_at`, `bid.expiration`, `bid.status`, and `bid.price`.
- Show buyer finalization entry points only for bids whose status is `Accepted` or `Contingent`; the backend enforces the same rule.
- Seller bid management endpoints now exist: `marketplace:seller_bid_list` at `seller/bids/` and `marketplace:update_seller_bid_status` as `POST` at `seller/bids/<pk>/status/`.
- `seller_bid_list.html` receives `seller`, `bids`, and `bid_status_choices`.
- Seller status update forms should post a valid `status` choice for the bid, include CSRF, and may include `next` for safe redirect-back behavior. Finalized bids cannot be changed; accepting one bid rejects competing bids for the same artwork.

## Finalization

- Start finalization with `marketplace:finalize_bid` at `bids/<pk>/finalize/`; it defaults to the `contact` step.
- Step-specific URLs use `marketplace:finalize_bid_step` with `bid.pk` and one of `contact`, `payment`, `review`, or `confirmation`.
- `finalize_contact.html` receives `bid`, `form`, `current_step`, `completed_steps`, and `finalization_steps`.
- `finalize_payment.html` receives `bid`, `form`, `current_step`, `completed_steps`, and `finalization_steps`; the backend redirects back to `contact` if contact data is missing.
- `finalize_review.html` receives `bid`, `contact`, `payment`, `current_step`, `completed_steps`, and `finalization_steps`; the backend redirects to missing earlier steps as needed.
- `finalize_confirmation.html` receives `bid`.
- Finalization data is kept in the user's session until review is confirmed. On confirmation, the backend creates or updates `BidFinalization`, marks it finalized, clears the session data, and redirects to `confirmation`.
- Already-finalized bids redirect to the `confirmation` step.
- `_finalization_steps.html` consumes `finalization_steps`. Each step dictionary has `key`, `label`, `url`, `is_current`, `is_enabled`, and `is_completed`.

## Encoding Audit

Scanned `marketplace/templates` for common mojibake markers. Current scan found no remaining artifacts.

- `marketplace/templates/marketplace/favorite_list.html:42` now uses `&middot;` between `{{ artwork.medium }}` and `{{ artwork.style }}`, which avoids the previously observed separator mojibake.
