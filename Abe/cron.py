# Cron for dump MN and Gov Info

from slickrpc import Proxy
import datetime
import json
import sys


rpc_user="rpsuser1"
rpc_password="IUSdHDiIUOPtrAWDSwDSIUDsdfGUgSF"



rpc_con = Proxy("http://%s:%s@127.0.0.1:9846"%(rpc_user, rpc_password))


def dump_mn_info():
    """Get Masternodes info"""
    mn = rpc_con.masternode("list", "full")
    # format
    # 'status protocol payee lastseen activeseconds lastpaidtime lastpaidblock IP'
    result = """
    {
      "data": [
    """
    for k in mn.keys():
        cr = mn[k].split(" ")
        cr = filter(lambda a: a != "", cr)
        cr[3] = datetime.datetime.fromtimestamp(int(cr[3])).strftime('%Y-%m-%d %H:%M:%S')
        cr[4] = str(datetime.timedelta(seconds=int(cr[4])))
        cr[5] = datetime.datetime.fromtimestamp(int(cr[5])).strftime('%Y-%m-%d %H:%M:%S')
        result += "\n %s," % json.dumps(cr)
    if result[-1] == ",":
        result = result[:-1]
    result += """
      ]
    }
    """
    print(result)


def dump_gov_info():
    """Get Governance info"""
    mn = rpc_con.gobject("list", "all")
    # format
    # 'status protocol payee lastseen activeseconds lastpaidtime lastpaidblock IP'
    result = []
    for k in mn.keys():
        cr_gob = mn[k]
        cr_prop = json.loads(cr_gob["DataString"])
        cr_prop = cr_prop[0][1]
        cr_gob["proposal"] = cr_prop
        del cr_gob["DataHex"]
        del cr_gob["DataString"]
        result.append(cr_gob)
    print(json.dumps(result))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("""Usage:
         # Masternodes Info
         python Abe/cron.py mn > Abe/htdocs/data/mn.json
         # Governance Info
         python Abe/cron.py gov > Abe/htdocs/data/gov.json
        """)
    elif sys.argv[1] == "mn":
        dump_mn_info()
    elif sys.argv[1] == "gov":
        dump_gov_info()
