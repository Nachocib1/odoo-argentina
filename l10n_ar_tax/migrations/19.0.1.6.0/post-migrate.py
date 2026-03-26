"""Assign 'See Payments Menu' group to users with accounting access.

l10n_ar_tax loads at position 296, after account_payment_pro (286)
which creates the group. Without this, no users can see the Pagos menu.
"""
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    cr.execute("""
        INSERT INTO res_groups_users_rel (gid, uid)
        SELECT g.id, r.uid
        FROM res_groups g
        CROSS JOIN res_groups_users_rel r
        WHERE g.name::text ILIKE '%%See Payments Menu%%'
          AND r.gid IN (
              SELECT id FROM res_groups
              WHERE name::text ILIKE '%%Invoicing%%'
                 OR name::text ILIKE '%%Facturación%%'
          )
        ON CONFLICT DO NOTHING
    """)
    _logger.info("post-migrate l10n_ar_tax: assigned payments menu group to %d user(s)", cr.rowcount)
