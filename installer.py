#!/usr/bin/env python3
import argparse
import os
import subprocess


def cprint(*args, level: int = 1):
	CRED = "\033[31m"
	CGRN = "\33[92m"
	CYLW = "\33[93m"
	reset = "\033[0m"
	message = " ".join(map(str, args))
	if level == 1:
		print(CRED, message, reset)
	if level == 2:
		print(CGRN, message, reset)
	if level == 3:
		print(CYLW, message, reset)


def main():
	parser = get_args_parser()
	args = parser.parse_args()
	init_bench_if_not_exist(args)
	create_site_in_bench(args)


def get_args_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"-j",
		"--apps-json",
		action="store",
		type=str,
		help="Path to apps.json, default: apps.json",
		default="apps.json",
	)
	parser.add_argument(
		"-b",
		"--bench-name",
		action="store",
		type=str,
		help="Bench directory name, default: frappe-bench",
		default="frappe-bench",
	)
	parser.add_argument(
		"-s",
		"--site-name",
		action="store",
		type=str,
		help="Site name, default: localhost",
		default="localhost",
	)
	parser.add_argument(
		"-r",
		"--root-password",
		action="store",
		type=str,
		help="Root password for MariaDB, default: 123",
		default="123",
	)
	parser.add_argument(
		"-a",
		"--admin-password",
		action="store",
		type=str,
		help="Admin password for site, default: admin",
		default="admin",
	)
	parser.add_argument(
		"-p",
		"--frappe-path",
		action="store",
		type=str,
		help="frappe repo path or url, default: https://github.com/frappe/frappe.git",
		default="https://github.com/frappe/frappe.git",
	)
	parser.add_argument(
		"--frappe-branch",
		action="store",
		type=str,
		help="frappe repo branch, default: version-16",
		default="version-16",
	)
	return parser


def init_bench_if_not_exist(args):
	if os.path.exists(args.bench_name):
		cprint(f"Directory {args.bench_name} already exists. Skipping bench init.", level=3)
		return

	cprint(f"Initializing bench: {args.bench_name}", level=2)
	bench_init_cmd = [
		"bench",
		"init",
		"--skip-redis-config-generation",
		"--frappe-path",
		args.frappe_path,
		"--frappe-branch",
		args.frappe_branch,
	]
	if os.path.exists(args.apps_json):
		bench_init_cmd.extend(["--apps-path", args.apps_json])

	bench_init_cmd.append(args.bench_name)
	subprocess.run(bench_init_cmd, check=True)

	# Configure Redis and MariaDB hosts
	subprocess.run(
		["bench", "set-config", "-g", "redis_cache", "redis://redis-cache:6379"],
		cwd=args.bench_name,
		check=True,
	)
	subprocess.run(
		["bench", "set-config", "-g", "redis_queue", "redis://redis-queue:6379"],
		cwd=args.bench_name,
		check=True,
	)
	subprocess.run(
		["bench", "set-config", "-g", "db_host", "mariadb"],
		cwd=args.bench_name,
		check=True,
	)


def create_site_in_bench(args):
	site_path = os.path.join(args.bench_name, "sites", args.site_name)
	if os.path.exists(site_path):
		cprint(f"Site {args.site_name} already exists in {args.bench_name}.", level=3)
		return

	cprint(f"Creating site {args.site_name}...", level=2)
	new_site_cmd = [
		"bench",
		"new-site",
		"--mariadb-root-username",
		"root",
		"--mariadb-root-password",
		args.root_password,
		"--admin-password",
		args.admin_password,
		"--no-mariadb-socket",
		args.site_name,
	]
	subprocess.run(new_site_cmd, cwd=args.bench_name, check=True)

	# Install apps from apps.json
	import json

	if os.path.exists(args.apps_json):
		with open(args.apps_json) as f:
			apps = json.load(f)
		for app in apps:
			app_url = app.get("url", "")
			app_name = app_url.rstrip("/").split("/")[-1].replace(".git", "")
			if app_name and app_name != "frappe":
				cprint(f"Installing app {app_name} on site {args.site_name}...", level=2)
				subprocess.run(
					["bench", "--site", args.site_name, "install-app", app_name],
					cwd=args.bench_name,
					check=True,
				)

	cprint(f"Site {args.site_name} created and configured successfully!", level=2)


if __name__ == "__main__":
	main()
