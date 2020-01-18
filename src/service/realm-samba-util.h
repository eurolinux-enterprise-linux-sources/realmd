/* realmd -- Realm configuration service
 *
 * Copyright 2012 Red Hat Inc
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published
 * by the Free Software Foundation; either version 2 of the licence or (at
 * your option) any later version.
 *
 * See the included COPYING file for more information.
 *
 * Author: Stef Walter <stefw@gnome.org>
 */

#include "config.h"

#ifndef __REALM_SAMBA_UTIL_H__
#define __REALM_SAMBA_UTIL_H__

#include <gio/gio.h>

G_BEGIN_DECLS

gchar *           realm_samba_util_build_strange_ou   (const gchar *ldap_dn,
                                                       const gchar *suffix_dn);

G_END_DECLS

#endif /* __REALM_SAMBA_UTIL_H__ */
