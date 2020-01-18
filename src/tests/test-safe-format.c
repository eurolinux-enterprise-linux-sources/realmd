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

#include "service/safe-format-string.h"

#include <glib.h>

#include <string.h>

typedef struct {
	const gchar *format;
	const gchar *args[8];
	const gchar *result;
} Fixture;

static void
callback (void *data,
          const char *piece,
          size_t len)
{
	g_string_append_len (data, piece, len);
}

static void
test_safe_format_string_cb (gconstpointer user_data)
{
	const Fixture *fixture = user_data;
	GString *out;
	int num_args;
	int ret;

	for (num_args = 0; fixture->args[num_args] != NULL; )
		num_args++;

	out = g_string_new ("");
	ret = safe_format_string_cb (callback, out, fixture->format, (const gchar **)fixture->args, num_args);
	if (fixture->result) {
		g_assert_cmpint (ret, >=, 0);
		g_assert_cmpstr (out->str, ==, fixture->result);
		g_assert_cmpint (ret, ==, out->len);
	} else {
		g_assert_cmpint (ret, <, 0);
	}

	g_string_free (out, TRUE);
}

static const Fixture fixtures[] = {
	{
	  /* Just a bog standard string */
	  "%s", { "blah", NULL, },
	  "blah"
	},
	{
	  /* Empty to print */
	  "%s", { "", NULL, },
	  ""
	},
	{
	  /* Nothing to print */
	  "", { "blah", NULL, },
	  ""
	},
	{
	  /* Width right aligned */
	  "%8s", { "blah", NULL, },
	  "    blah"
	},
	{
	  /* Width left aligned */
	  "whoop %-8s doo", { "dee", NULL, },
	  "whoop dee      doo"
	},
	{
	  /* Width space aligned (ignored) */
	  "whoop % 8s doo", { "dee", NULL, },
	  "whoop      dee doo"
	},
	{
	  /* Width left space aligned (ignored) */
	  "whoop % -8s doo", { "dee", NULL, },
	  "whoop dee      doo"
	},
	{
	  /* Precision 1 digit */
	  "whoop %.3s doo", { "deedle-dee", NULL, },
	  "whoop dee doo"
	},
	{
	  /* Precision, N digits */
	  "whoop %.10s doo", { "deedle-dee-deedle-do-deedle-dum", NULL, },
	  "whoop deedle-dee doo"
	},
	{
	  /* Precision, zero digits */
	  "whoop %.s doo", { "deedle", NULL, },
	  "whoop  doo"
	},
	{
	  /* Multiple simple arguments */
	  "space %s %s", { "man", "dances", NULL, },
	  "space man dances"
	},
	{
	  /* Literal percent */
	  "100%% of space folk dance", { NULL, },
	  "100% of space folk dance"
	},
	{
	  /* Multiple simple arguments */
	  "space %2$s %1$s", { "dances", "man", NULL, },
	  "space man dances"
	},
	{
	  /* Skipping an argument (not supported by standard printf) */
	  "space %2$s dances", { "dances", "man", NULL, },
	  "space man dances"
	},

	/* Failures start here */

	{
	  /* Unsupported conversion */
	  "%x", { "blah", NULL, },
	  NULL
	},
	{
	  /* Bad positional argument */
	  "space %55$s dances", { "dances", "man", NULL, },
	  NULL
	},
	{
	  /* Zero positional argument */
	  "space %0$s dances", { "dances", "man", NULL, },
	  NULL
	},
	{
	  /* Too many args used */
	  "%s %s dances", { "space", NULL, },
	  NULL
	},

};

static void
test_safe_format_string (void)
{
	char buffer[8];
	int ret;

	ret = safe_format_string (buffer, 8, "%s", "space", "man", NULL);
	g_assert_cmpint (ret, ==, 5);
	g_assert_cmpstr (buffer, ==, "space");

	ret = safe_format_string (buffer, 8, "", "space", "man", NULL);
	g_assert_cmpint (ret, ==, 0);
	g_assert_cmpstr (buffer, ==, "");

	ret = safe_format_string (buffer, 8, "the %s %s dances away", "space", "man", NULL);
	g_assert_cmpint (ret, ==, 25);
	g_assert_cmpstr (buffer, ==, "the spa");

	ret = safe_format_string (buffer, 8, "%5$s", NULL);
	g_assert_cmpint (ret, <, 0);
}

int
main (int argc,
      char **argv)
{
	gchar *escaped;
	gchar *name;
	gint i;

	g_test_init (&argc, &argv, NULL);
	g_set_prgname ("test-safe-format");

	for (i = 0; i < G_N_ELEMENTS (fixtures); i++) {
		if (g_str_equal (fixtures[i].format, ""))
			escaped = g_strdup ("_empty_");
		else
			escaped = g_strdup (fixtures[i].format);
		g_strdelimit (escaped, " =\\/", '_');
		name = g_strdup_printf ("/realmd/safe-format/%s", escaped);
		g_free (escaped);

		g_test_add_data_func (name, fixtures + i, test_safe_format_string_cb);
		g_free (name);
	}

	g_test_add_func ("/realmd/safe-format-string", test_safe_format_string);

	return g_test_run ();
}
