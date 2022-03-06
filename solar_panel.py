# SWAMI KARUPPASWAMI THUNNAI

import secrets
from flask import Flask
from flask import redirect
from inventory.inventory import inventory
from inventory.api import *
from flask_restful import Resource,Api
from flask_cors import CORS
from flask import request, redirect, url_for, session,flash,jsonify
from werkzeug.utils import secure_filename
import os
from flask_toastr import Toastr

app = Flask(__name__)
app.secret_key = "TEMPKEYFORTESTING"
CORS(app)

api=Api(app)
toastr = Toastr(app)

app.register_blueprint(inventory)

	# ============================================ api's ========================================

# -------------------------------------------- Login ----------------------------------------
api.add_resource(login, "/api/login")

# -------------------------------------------- Login Out -------------------------------------
api.add_resource(logout, "/api/logout")

	# ============================================ super_admin  ========================================

# -------------------------------------------- Create super admin ----------------------------
api.add_resource(create_super_admin, "/api/create_super_admin")

# -------------------------------------------- Edit super admin ----------------------------
api.add_resource(edit_super_admin, "/api/edit_super_admin")

# -------------------------------------------- Status super admin ----------------------------
api.add_resource(status_super_admin, "/api/status_super_admin")

# -------------------------------------------- view super admin ----------------------------
api.add_resource(view_super_admin, "/api/view_super_admin")

	# ============================================ admin  ========================================

# -------------------------------------------- Create admin ----------------------------
api.add_resource(create_admin, "/api/create_admin")

# -------------------------------------------- view admin_group ----------------------------
api.add_resource(view_admin, "/api/view_admin")

# -------------------------------------------- Edit admin ----------------------------
api.add_resource(edit_admin, "/api/edit_admin")

# -------------------------------------------- Status admin ----------------------------
api.add_resource(status_admin, "/api/status_admin")

	# ============================================ admin group  ========================================

# -------------------------------------------- Create admin_group ----------------------------
api.add_resource(create_admin_group, "/api/create_admin_group")

# -------------------------------------------- view admin_group ----------------------------
api.add_resource(view_admin_group, "/api/view_admin_group")

# -------------------------------------------- Edit admin_group ----------------------------
api.add_resource(edit_admin_group, "/api/edit_admin_group")

# -------------------------------------------- Status admin_group ----------------------------
api.add_resource(status_admin_group, "/api/status_admin_group")

	# ============================================ support  ========================================
	
# -------------------------------------------- Create support ----------------------------
api.add_resource(create_support, "/api/create_support")

# -------------------------------------------- view support ----------------------------
api.add_resource(view_support, "/api/view_support")

# -------------------------------------------- Edit support ----------------------------
api.add_resource(edit_support, "/api/edit_support")
# -------------------------------------------- view alloted to ----------------------------

api.add_resource(view_alloted_to, "/api/view_alloted_to")

api.add_resource(user_admin, "/api/user_admin")

# ============================================ catagory  ========================================
# -------------------------------------------- Create catagory ----------------------------
api.add_resource(create_catagory, "/api/create_catagory")
# -------------------------------------------- view catagory ----------------------------
api.add_resource(view_catagory, "/api/view_catagory")


# ============================================ users  ========================================
# -------------------------------------------- Create users ----------------------------
api.add_resource(create_users, "/api/create_users")
# -------------------------------------------- view users ----------------------------
api.add_resource(view_users, "/api/view_users")

	# ============================================ accounts  ========================================
	
# -------------------------------------------- Create accounts ----------------------------
api.add_resource(create_accounts, "/api/create_accounts")
# -------------------------------------------- view accounts ----------------------------
api.add_resource(view_accounts, "/api/view_accounts")

# -------------------------------------------- Edit accounts ----------------------------
api.add_resource(edit_accounts, "/api/edit_accounts")

# -------------------------------------------- status accounts ----------------------------
api.add_resource(status_accounts, "/api/status_accounts")

	# ============================================ inverter  ========================================

# -------------------------------------------- Create inverter ----------------------------
api.add_resource(create_inverter, "/api/create_inverter")

# -------------------------------------------- view inverter ----------------------------
api.add_resource(view_inverter, "/api/view_inverter")
# -------------------------------------------- view inverter ----------------------------
api.add_resource(admin_view_inverter, "/api/admin_view_inverter")
# -------------------------------------------- Edit inverter ----------------------------
api.add_resource(edit_inverter, "/api/edit_inverter")

# -------------------------------------------- Status inverter ----------------------------
api.add_resource(status_inverter, "/api/status_inverter")

	# ============================================ smb  ========================================

# -------------------------------------------- Create smb ----------------------------
api.add_resource(create_smb, "/api/create_smb")

# -------------------------------------------- view smb ----------------------------
api.add_resource(view_smb, "/api/view_smb")
# -------------------------------------------- view smb ----------------------------
api.add_resource(admin_view_smb, "/api/admin_view_smb")

# -------------------------------------------- Edit smb ----------------------------
api.add_resource(edit_smb, "/api/edit_smb")

# -------------------------------------------- Status smb ----------------------------
api.add_resource(status_smb, "/api/status_smb")


# ============================================ energy meter  ========================================

# -------------------------------------------- Create energy_meter ----------------------------
api.add_resource(create_energy_meter, "/api/create_energy_meter")

# -------------------------------------------- view energy_meter ----------------------------
api.add_resource(view_energy_meter, "/api/view_energy_meter")

# -------------------------------------------- view energy_meter ----------------------------
api.add_resource(admin_view_energy_meter, "/api/admin_view_energy_meter")

# -------------------------------------------- Edit energy_meter ----------------------------
api.add_resource(edit_energy_meter, "/api/edit_energy_meter")

# -------------------------------------------- Status energy_meter ----------------------------
api.add_resource(status_energy_meter, "/api/status_energy_meter")


# ============================================ gateway  ========================================

# -------------------------------------------- Create gateway ----------------------------
api.add_resource(create_gateway, "/api/create_gateway")

# -------------------------------------------- view gateway ----------------------------
api.add_resource(view_gateway, "/api/view_gateway")
# -------------------------------------------- admin view gateway ----------------------------
api.add_resource(admin_view_gateway, "/api/admin_view_gateway")
# -------------------------------------------- Edit gateway ----------------------------
api.add_resource(edit_gateway, "/api/edit_gateway")

# -------------------------------------------- Status gateway ----------------------------
api.add_resource(status_gateway, "/api/status_gateway")


# ============================================ w & w  ========================================

# -------------------------------------------- Create w_w ----------------------------
api.add_resource(create_w_w, "/api/create_w_w")

# -------------------------------------------- view w_w ----------------------------
api.add_resource(view_w_w, "/api/view_w_w")

# -------------------------------------------- admin_view_w_w ----------------------------
api.add_resource(admin_view_w_w, "/api/admin_view_w_w")
api.add_resource(super_admin_view_w_w, "/api/super_admin_view_w_w")

# -------------------------------------------- Edit w_w ----------------------------
api.add_resource(edit_w_w, "/api/edit_w_w")

# -------------------------------------------- Status w_w ----------------------------
api.add_resource(status_w_w, "/api/status_w_w")



	# ============================================ rolls ========================================

# -------------------------------------------- Create rolls-----------------------------
api.add_resource(create_roll, "/api/create_roll")

# -------------------------------------------- view rolls-----------------------------
api.add_resource(view_roll, "/api/view_roll")

# -------------------------------------------- Edit rolls-----------------------------
api.add_resource(edit_roll, "/api/edit_roll")

# -------------------------------------------- Status rolls-----------------------------
api.add_resource(status_roll, "/api/status_roll")

# -------------------------------------------- solar_panel_data-----------------------------
api.add_resource(solar_panel_data, "/api/solar_panel_data")

api.add_resource(abj_solar_panel_data, "/api/abj_solar_panel_data")

api.add_resource(current_solar_panel_data, "/api/current_solar_panel_data")

api.add_resource(inverter_solar_panel_data, "/api/inverter_solar_panel_data")

api.add_resource(inverter_solar_panel_data_, "/api/inverter_solar_panel_data_")

api.add_resource(engerymeter_solar_panel_data, "/api/engerymeter_solar_panel_data")

api.add_resource(w_w_solar_panel_data, "/api/w_w_solar_panel_data")

api.add_resource(data_visual, "/api/data_visual")

api.add_resource(data_visual_graph, "/api/data_visual_graph")
@app.route("/")
def index():
    return redirect("/solar_panel")


if __name__ == "__main__":
    app.run(debug=True)
